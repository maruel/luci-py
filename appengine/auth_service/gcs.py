# Copyright 2019 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Helpers for managing AuthDB dump in Google Cloud Storage."""

import logging

from google.appengine.ext import ndb

from components import auth
from components import net
from components import utils

import acl
import config


class Error(Exception):
  """Raised on fatal errors when calling Google Storage."""


def is_authorized_reader(email):
  """True if the given user is allowed to fetch AuthDB Google Storage file."""
  return bool(_auth_db_reader_key(email).get())


def authorize_reader(email):
  """Allows the given user to fetch AuthDB Google Storage file."""
  reader = AuthDBReader(
      key=_auth_db_reader_key(email),
      authorized_at=utils.utcnow())
  reader.put()
  _update_gcs_acls()


def deauthorize_reader(email):
  """Revokes the authorization to fetch AuthDB Google Storage file."""
  _auth_db_reader_key(email).delete()
  _update_gcs_acls()


def revoke_stale_authorization():
  """Removes authorization from accounts that no longer have access."""
  to_delete = []
  for email in _list_authorized_readers():
    ident = auth.Identity.from_bytes('user:' + email)
    if not acl.is_trusted_service(ident):
      logging.warning('Removing "%s" as authorized GCS reader', email)
      to_delete.append(_auth_db_reader_key(email))
  if to_delete:
    ndb.delete_multi(to_delete)
    _update_gcs_acls()


def is_upload_enabled():
  """True if uploads to GCS are enabled in the config."""
  return bool(config.get_settings().auth_db_gs_path)


def upload_auth_db(signed_auth_db, revision_json):
  """Updates Google Storage files to contain the latest AuthDB.

  Will write two Google Storage objects (in that order):
    * <auth_db_gs_path>/latest.db: binary-serialized SignedAuthDB.
    * <auth_db_gs_path>/latest.json: JSON-serialized AuthDBRevision.

  Where <auth_db_gs_path> is taken from 'auth_db_gs_path' in SettingsCfg in
  config.proto.

  Each individual file write is atomic, but it is possible latest.db is updated
  but latest.json is not (i.e. if the call crashes in between two writes). If
  this happens, 'upload_auth_db' should be retried. Eventually both files should
  agree.

  Args:
    signed_auth_db: binary-serialized SignedAuthDB proto message.
    revision_json: JSON-serialized AuthDBRevision proto message.

  Raises:
    net.Error if Google Storage writes fail.
  """
  gs_path = config.get_settings().auth_db_gs_path
  if not gs_path:
    return
  assert not gs_path.endswith('/'), gs_path
  readers = _list_authorized_readers()
  _upload_file(
      path=gs_path+'/latest.db',
      data=signed_auth_db,
      content_type='application/protobuf',
      readers=readers)
  _upload_file(
      path=gs_path+'/latest.json',
      data=revision_json,
      content_type='application/json',
      readers=readers)


### Private stuff.


class AuthDBReader(ndb.Model):
  """Account that should be able to read AuthDB Google Storage dump.

  These are accounts that have explicitly requested access to the AuthDB via
  /auth_service/api/v1/authdb/subscription/authorization API call.

  They all belong to 'auth-trusted-services' group (see acl.is_trusted_service).
  Note that we can't just authorize all members of 'auth-trusted-services' since
  in general we can't even enumerate them (for example, there's no way to
  enumerate glob entries like *@example.com).

  Parent entity key is always _auth_db_readers_root_key(). Entity ID is the
  account email. Use _auth_db_reader_key() to construct the entity key.
  """
  authorized_at = ndb.DateTimeProperty(indexed=False)


def _auth_db_readers_root_key():
  """Root key for AuthDBReader entities. The entity itself doesn't exist."""
  return ndb.Key('AuthDBReadersRoot', 'root')


def _auth_db_reader_key(email):
  """Returns ndb.Key of some AuthDBReader entity."""
  return ndb.Key(AuthDBReader, email, parent=_auth_db_readers_root_key())


def _list_authorized_readers():
  """Returns emails of all readers authorized via AuthDBReader entity."""
  q = AuthDBReader.query(ancestor=_auth_db_readers_root_key())
  return sorted(key.id() for key in q.fetch(keys_only=True))


def _upload_file(path, data, content_type, readers):
  """Overwrites a file in GCS, makes it readable to all authorized readers.

  Doesn't use streaming uploads currently. Data is limited by URL Fetch request
  size (10 MB).

  Args:
    path: "<bucket>/<object>" string.
    data: buffer with data to upload.
    content_type: MIME content type of 'data', to put into GCS metadata.
    readers: list of emails that should have read access to the file.

  Raises:
    Error if Google Storage writes fail.
  """
  # See https://cloud.google.com/storage/docs/json_api/v1/how-tos/simple-upload.
  bucket, name = path.split('/', 1)
  try:
    # TODO(vadimsh): Set ACLs based on 'readers'.
    net.request(
        url='https://www.googleapis.com/upload/storage/v1/b/%s/o' % bucket,
        method='POST',
        payload=data,
        params={'uploadType': 'media', 'name': name},
        headers={'Content-Type': content_type},
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
        deadline=30)
  except net.Error as exc:
    raise Error(str(exc))


def _update_gcs_acls():
  """Changes ACLs of existing GCS files to match what's in AuthDBReader list.

  Can be mocked in tests.
  """
  # TODO(vadimsh): Implement.
