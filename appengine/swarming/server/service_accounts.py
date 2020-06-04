# Copyright 2017 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Functions to generate OAuth access tokens to use by bots or inside tasks."""

import collections
import datetime
import logging
import os
import random
import re

from google.appengine.api import app_identity
from google.appengine.api import memcache

from components import auth
from components import net
from components import utils

from server import task_pack


# Brackets for possible lifetimes of OAuth tokens produced by this module.
MIN_TOKEN_LIFETIME_SEC = 5 * 60
MAX_TOKEN_LIFETIME_SEC = 3600 * 60  # this is just hardcoded by Google APIs

AccessToken = collections.namedtuple(
    'AccessToken',
    [
        'access_token',  # actual access token
        'expiry',  # unix timestamp (in seconds, int) when it expires
    ])


class PermissionError(Exception):
  """The service account is not allowed to be used by the caller."""


class MisconfigurationError(Exception):
  """Something is not correctly configured.

  The difference from PermissionError is that generally the account is allowed
  to be used, but some misconfiguration (e.g. IAM permissions) preclude the
  token server or Swarming from using it.

  Can be transformed into HTTP 400 error and returned to the caller.
  """


class InternalError(Exception):
  """Something unexpectedly misbehaves.

  This generally should not happen. It's fine to return HTTP 500 if it does. The
  content of the exception is scabbed of private information that should not be
  visible to the caller.
  """


def has_token_server():
  """Returns True if Token Server URL is configured.

  Token Server is required to use task-associated service accounts.
  """
  return bool(auth.get_request_auth_db().token_server_url)


def is_service_account(value):
  """Returns True if given value looks like a service account email."""
  return bool(_SERVICE_ACCOUNT_RE.match(value))


def get_oauth_token_grant(service_account, validity_duration):
  """Returns "OAuth token grant" that allows usage of the service account.

  OAuth token grant is a signed assertion that basically says "the token server
  approves the usage of <service_account> by the <end-user>, and this assertion
  is valid for <validity_duration>".

  This function is called when the task is posted, while the end-user is still
  present. The grant it either generated by contacting the token server or
  fetched from the cache (if the cached one lives long enough).

  This function must not be used if 'has_token_server()' returns False. It will
  raise assertion error.

  The grant is later passed back to the token server to generate an actual OAuth
  access token. When this happens, the token server rechecks the ACLs, so it's
  fine to have large 'validity_duration' here. It basically defines for how long
  to cache "positive" ACL check.

  Args:
    service_account: a service account email to use.
    validity_duration: timedelta with how long the returned grant should live.

  Returns:
    Base64-encoded string with the grant body.

  Raises:
    PermissionError if the token server forbids the usage.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  assert has_token_server()
  assert is_service_account(service_account), service_account

  end_user = auth.get_current_identity()

  existing_grant = None
  existing_exp_ts = None

  # Try to find a cached token first.
  cache_key = _oauth_token_grant_cache_key(service_account, end_user)
  cached = memcache.get(cache_key, namespace=_OAUTH_TOKEN_GRANT_CACHE_NS)
  if cached:
    try:
      existing_grant = cached['oauth_token_grant']
      existing_exp_ts = utils.timestamp_to_datetime(cached['exp_ts'])
      if not isinstance(existing_grant, str):
        raise TypeError('"oauth_token_grant" should be str')
    except (KeyError, ValueError, TypeError):
      # Treat malformed data as a cache miss. This should not happen generally.
      logging.exception('Failed to parse oauth token grant cache entry: %s')
      existing_grant = None
      existing_exp_ts = None

  # Randomly "expire" a cached token a bit prematurely to avoid a storm of
  # refresh requests when it expires for everyone for real. With a randomization
  # only few unlucky requests (most likely one) will hit the token refresh
  # procedure.
  now = utils.utcnow()
  if existing_exp_ts:
    rnd = datetime.timedelta(seconds=random.randint(0, 600))
    if now > existing_exp_ts - rnd:
      existing_grant = None
      existing_exp_ts = None

  # Does the cached token live long enough to be useful for the caller?
  if existing_exp_ts and existing_exp_ts > now + validity_duration:
    _log_token_grant('Using cached', existing_grant, existing_exp_ts)
    return existing_grant

  # Need to make a new token either because the cached one has expired or it
  # doesn't live long enough.
  #
  # We give the new token 1h of extra lifetime to make sure it can be reused by
  # next ~1h worth of tasks (assuming all tasks request exact same lifetime).
  # Without this trick each new task will attempt to generate new token, seeing
  # that the cached one expired just a few moments ago. With 1h extra lifetime
  # we effectively cache the token for 1h (minus 0-10 min due to the expiration
  # randomization above).
  #
  # Note: this call raises auth.AuthorizationError if the current caller is not
  # allowed to use the service account.
  new_grant, new_exp_ts = _mint_oauth_token_grant(
      service_account, end_user,
      validity_duration + datetime.timedelta(hours=1))

  # Verify the token server produces a token that lives long enough. The expiry
  # of new token must surely be above validity_duration, since we request 1h of
  # extra life.
  if new_exp_ts < now + validity_duration:
    _log_token_grant(
        'Got unexpectedly short-lived',
        new_grant,
        new_exp_ts,
        log_call=logging.error)
    raise InternalError('Got unexpectedly short-lived grant, see server logs')

  # New token is good.
  memcache.set(
      key=cache_key,
      value={
          'oauth_token_grant': new_grant,
          'exp_ts': utils.datetime_to_timestamp(new_exp_ts),
      },
      time=utils.datetime_to_timestamp(new_exp_ts) / 1e6,
      namespace=_OAUTH_TOKEN_GRANT_CACHE_NS)

  _log_token_grant('Generated new', new_grant, new_exp_ts)
  return new_grant


def get_task_account_token(task_id, bot_id, scopes):
  """Returns an access token for a service account associated with a task.

  Assumes authorization checks have been made already. If the task is not
  configured to use service account returns ('none', None). If the task is
  configured to use whatever bot is using when calling Swarming, returns
  ('bot', None).

  Otherwise returns (<email>, AccessToken with valid token for <email>).

  If the task has realm, it calls MintServiceAccountToken rpc using the realm.
  Otherwise, it calls MintOAuthTokenViaGrant with grant token. The legacy path
  will be deprecated after migrating to Realm-based configurations.

  Args:
    task_id: ID of the task.
    bot_id: ID of the bot that executes the task, for logs.
    scopes: list of requested OAuth scopes.

  Returns:
    (<service account email> or 'bot' or 'none', AccessToken or None).

  Raises:
    PermissionError if the token server forbids the usage.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  # Grab corresponding TaskRequest.
  try:
    result_summary_key = task_pack.run_result_key_to_result_summary_key(
        task_pack.unpack_run_result_key(task_id))
    task_request_key = task_pack.result_summary_key_to_request_key(
        result_summary_key)
  except ValueError as exc:
    logging.error('Unexpectedly bad task_id: %s', exc)
    raise MisconfigurationError('Bad task_id: %s' % task_id)

  task_request = task_request_key.get()
  if not task_request:
    raise MisconfigurationError('No such task request: %s' % task_id)

  # 'none' or 'bot' cases are handled by the bot locally, no token for them.
  if task_request.service_account in ('none', 'bot'):
    return task_request.service_account, None

  # The only possible case is a service account email. Double check this.
  if not is_service_account(task_request.service_account):
    raise MisconfigurationError(
        'Not a service account email: %s' % task_request.service_account)

  # Additional information for Token Server's logs.
  audit_tags = [
      'swarming:bot_id:%s' % bot_id,
      'swarming:task_id:%s' % task_id,
      'swarming:task_name:%s' % task_request.name,
  ]

  if task_request.realm:
    # If TaskRequest.realm is set, it calls MintServiceAccountToken to grab
    # a OAuth token. It re-checks swarming.tasks.runAs permission before
    # calling the RPC because the permission may have been removed since
    # the last check.
    access_token, expiry = _mint_service_account_token(
        task_request.service_account, task_request.realm, scopes, audit_tags)
  else:
    # Should have a token prepared by 'get_oauth_token_grant' already.
    if not task_request.service_account_token:
      raise MisconfigurationError(
          'The task request %s has no associated service account token'
          % task_id)

    # Use this token to grab the real OAuth token. Note that the bot caches the
    # resulting OAuth token internally, so we don't bother to cache it here.
    access_token, expiry = _mint_oauth_token_via_grant(
        task_request.service_account_token, scopes, audit_tags)

  # Log and return the token.
  token = AccessToken(access_token,
                      int(utils.datetime_to_timestamp(expiry) / 1e6))
  _check_and_log_token('task associated', task_request.service_account, token)
  return task_request.service_account, token


def get_system_account_token(system_service_account, scopes):
  """Returns an access token to use on bots when calling internal services.

  "Internal services" are (loosely) everything that is needed for correct
  functioning of the internal guts of the bot (at least Isolate and CIPD).

  Assumes authorization checks have been made already. If the bot is not
  configured to use service account returns ('none', None). If the bot is
  configured to use whatever it is using when calling Swarming itself, returns
  ('bot', None).

  Otherwise returns (<email>, AccessToken with valid token for <email>).

  Args:
    system_service_account: whatever is specified in bots.cfg for the bot.
    scopes: list of requested OAuth scopes.

  Returns:
    (<service account email> or 'bot' or 'none', AccessToken or None).

  Raises:
    PermissionError if the usage of the account is forbidden.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  if not system_service_account:
    return 'none', None  # no auth is configured

  if system_service_account == 'bot':
    return 'bot', None  # the bot should use tokens provided by local hooks

  # Attempt to mint a token (or grab an existing one from cache).
  try:
    blob, expiry = auth.get_access_token(
        scopes=scopes,
        act_as=system_service_account,
        min_lifetime_sec=MIN_TOKEN_LIFETIME_SEC)
  except auth.AccessTokenError as exc:
    if exc.transient:
      raise InternalError(exc.message)
    raise MisconfigurationError(exc.message)

  assert isinstance(blob, basestring)
  assert isinstance(expiry, (int, long, float))
  token = AccessToken(blob, int(expiry))
  _check_and_log_token('bot associated', system_service_account, token)
  return system_service_account, token


### Private code


# Matches service account email (or rather close enough superset of it).
_SERVICE_ACCOUNT_RE = re.compile(r'^[0-9a-zA-Z_\-\.\+\%]+@[0-9a-zA-Z_\-\.]+$')

# Memcache namespace for OAuth token grants.
_OAUTH_TOKEN_GRANT_CACHE_NS = 'oauth_token_grants_v1'


def _oauth_token_grant_cache_key(service_account, end_user):
  """Returns a memcache key for cached OAuth token grant."""
  assert '|' not in service_account, service_account
  return '%s|%s' % (service_account, end_user.to_bytes())


def _mint_oauth_token_grant(service_account, end_user, validity_duration):
  """Does the actual RPC to the token server to generate OAuth token grant.

  Args:
    service_account: a service account email to use.
    end_user: identity of the end user (the one who posts Swarming task).
    validity_duration: timedelta with how long the returned token should live.

  Returns:
    (new token, datetime when it expires).

  Raises:
    PermissionError if the token server forbids the usage.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  resp = _call_token_server(
      'MintOAuthTokenGrant', {
          'serviceAccount': service_account,
          'validityDuration': int(validity_duration.total_seconds()),
          'endUser': end_user.to_bytes(),
          'auditTags': _common_audit_tags(),
      })
  try:
    grant_token = str(resp['grantToken'])
    service_version = str(resp['serviceVersion'])
    expiry = utils.parse_rfc3339_datetime(resp['expiry'])
  except (KeyError, ValueError) as exc:
    logging.error('Bad response from the token server (%s):\n%r', exc, resp)
    raise InternalError('Bad response from the token server, see server logs')
  logging.info('The token server replied, its version: %s', service_version)
  return grant_token, expiry


def _mint_oauth_token_via_grant(grant_token, oauth_scopes, audit_tags):
  """Does the RPC to the token server to exchange a grant for an access token.

  Args:
    grant_token: a token generated by get_oauth_token_grant.
    oauth_scopes: list of strings with requested OAuth scopes.
    audit_tags: list with information tags to send with the RPC, for logging.

  Returns:
    (new token, datetime when it expires).

  Raises:
    PermissionError if the token server forbids the usage.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  resp = _call_token_server(
      'MintOAuthTokenViaGrant', {
          'grantToken': grant_token,
          'oauthScope': oauth_scopes,
          'minValidityDuration': MIN_TOKEN_LIFETIME_SEC,
          'auditTags': _common_audit_tags() + audit_tags,
      })
  try:
    access_token = str(resp['accessToken'])
    service_version = str(resp['serviceVersion'])
    expiry = utils.parse_rfc3339_datetime(resp['expiry'])
  except (KeyError, ValueError) as exc:
    logging.error('Bad response from the token server (%s):\n%r', exc, resp)
    raise InternalError('Bad response from the token server, see server logs')
  logging.info('The token server replied, its version: %s', service_version)
  return access_token, expiry


def _mint_service_account_token(service_account, realm, oauth_scopes,
                                audit_tags):
  """Does the RPC to the token server to get an access token using realm.

  Args:
    service_account: a service account email to use.
    realm: a realm name to use.
    oauth_scopes: list of strings with requested OAuth scopes.
    audit_tags: list with information tags to send with the RPC, for logging.

  Raises:
    PermissionError if the token server forbids the usage.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  resp = _call_token_server(
      'MintServiceAccountToken',
      {
          # tokenserver.minter.SERVICE_ACCOUNT_TOKEN_ACCESS_TOKEN
          'tokenKind': 1,
          'serviceAccount': service_account,
          'realm': realm,
          'oauthScopes': oauth_scopes,
          'auditTags': _common_audit_tags() + audit_tags,
      })
  try:
    access_token = str(resp['token'])
    service_version = str(resp['serviceVersion'])
    expiry = utils.parse_rfc3339_datetime(resp['expiry'])
  except (KeyError, ValueError) as exc:
    logging.error('Bad response from the token server (%s):\n%r', exc, resp)
    raise InternalError('Bad response from the token server, see server logs')
  logging.info('The token server replied, its version: %s', service_version)
  return access_token, expiry


def _call_token_server(method, request):
  """Sends an RPC to tokenserver.minter.TokenMinter service.

  Args:
    method: name of the method to call.
    request: dict with request fields.

  Returns:
    Dict with response fields.

  Raises:
    PermissionError on HTTP 403 reply.
    MisconfigurationError if the service account is misconfigured.
    InternalError if the RPC fails unexpectedly.
  """
  # Double check token server URL looks sane ('https://....'). This is checked
  # when it's imported from the config. This check should never fail.
  ts_url = auth.get_request_auth_db().token_server_url
  try:
    utils.validate_root_service_url(ts_url)
  except ValueError as exc:
    raise MisconfigurationError(
        'Invalid token server URL %s: %s' % (ts_url, exc))

  # See TokenMinter in
  # https://chromium.googlesource.com/infra/luci/luci-go/+/master/tokenserver/api/minter/v1/token_minter.proto
  # But beware that proto JSON serialization uses camelCase, not snake_case.
  try:
    return net.json_request(
        url='%s/prpc/tokenserver.minter.TokenMinter/%s' % (ts_url, method),
        method='POST',
        payload=request,
        scopes=[net.EMAIL_SCOPE])
  except net.Error as exc:
    logging.error('Error calling %s (HTTP %s: %s):\n%s', method,
                  exc.status_code, exc.message, exc.response)
    if exc.status_code == 403:
      raise PermissionError(
          'HTTP 403 from the token server:\n%s' % exc.response)
    if exc.status_code == 400:
      raise MisconfigurationError(
          'HTTP 400 from the token server:\n%s' % exc.response)
    # Don't put the response body into the error message, it may contain
    # internal details (that are public to Swarming server, but may not be
    # public to whoever is calling the Swarming server now).
    raise InternalError('Failed to call %s, see server logs' % method)


def _common_audit_tags():
  """Returns a list of tags that describe circumstances of the RPC call.

  They end up in Token Server's logs and can be used to correlate token server
  requests to Swarming requests.
  """
  # Note: particular names and format of tags is chosen to be consistent with
  # Token Server's logging.
  return [
      'swarming:gae_request_id:%s' % os.getenv('REQUEST_LOG_ID', '?'),
      'swarming:service_version:%s/%s' % (app_identity.get_application_id(),
                                          utils.get_app_version()),
  ]


def _log_token_grant(prefix, token, exp_ts, log_call=logging.info):
  """Logs details about an OAuth token grant."""
  ts = utils.datetime_to_timestamp(exp_ts)/1e6
  log_call(
      '%s OAuth token grant: fingerprint=%s, expiry=%d, expiry_in=%d', prefix,
      utils.get_token_fingerprint(token), ts, ts - utils.time_time())


def _check_and_log_token(flavor, account_email, token):
  """Checks the lifetime and logs details about the generated access token."""
  expires_in = token.expiry - utils.time_time()
  logging.info(
      'Got %s access token: email=%s, fingerprint=%s, expiry=%d, expiry_in=%d',
      flavor, account_email, utils.get_token_fingerprint(token.access_token),
      token.expiry, expires_in)
  # Give 2 min of wiggle room to account for various effects related to
  # relativity of clocks (us vs Google backends that produce the token) and
  # indeterminism of network propagation delays. 2 min should be more than
  # enough to account for them. These asserts should never be hit.
  assert expires_in < MAX_TOKEN_LIFETIME_SEC + 60
  assert expires_in > MIN_TOKEN_LIFETIME_SEC - 60
