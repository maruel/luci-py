# Copyright 2015 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Provides info about projects (service tenants)."""

import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages

from components.config.proto import project_config_pb2
from components.config.proto import service_config_pb2

import common
import storage


DEFAULT_REF_CFG = project_config_pb2.RefsCfg(
    refs=[project_config_pb2.RefsCfg.Ref(name='refs/heads/master')])


class RepositoryType(messages.Enum):
  GITILES = 1


class ProjectImportInfo(ndb.Model):
  """Contains info how a project was imported.

  Entity key:
    Id is project id from the project registry. Has no parent.
  """
  created_ts = ndb.DateTimeProperty(auto_now_add=True)
  repo_type = msgprop.EnumProperty(RepositoryType, required=True)
  repo_url = ndb.StringProperty(required=True)


@ndb.transactional
def update_import_info(project_id, repo_type, repo_url):
  """Updates ProjectImportInfo if needed."""
  info = ProjectImportInfo.get_by_id(project_id)
  if info and info.repo_type == repo_type and info.repo_url == repo_url:
    return
  if info:
    values = (
      ('repo_url', repo_url, info.repo_url),
      ('repo_type', repo_type, info.repo_type),
    )
    logging.warning('Changing project %s repo info:\n%s',
        project_id,
        '\n'.join([
          '%s: %s -> %s' % (attr, old_value, new_value)
          for attr, old_value, new_value in values
          if old_value != new_value
        ]))
  ProjectImportInfo(id=project_id, repo_type=repo_type, repo_url=repo_url).put()


def get_projects():
  """Returns a list of projects stored in services/luci-config:projects.cfg.

  Never returns None. Cached.
  """
  cfg = storage.get_self_config_async(
      common.PROJECT_REGISTRY_FILENAME,
      service_config_pb2.ProjectsCfg).get_result()
  return cfg.projects or []


def get_project(id):
  """Returns a project by id."""
  for p in get_projects():
    if p.id == id:
      return p
  return None


def get_repos(project_ids):
  """Returns a mapping {project_id: (repo_type, repo_url)}.

  All projects must exist.
  """
  assert isinstance(project_ids, list)
  keys = [ndb.Key(ProjectImportInfo, pid) for pid in project_ids]
  return {
    pid: (info.repo_type, info.repo_url) if info else (None, None)
    for pid, info in zip(project_ids, ndb.get_multi(keys))
  }


def get_metadata(project_ids):
  """Returns a mapping {project_id: metadata}.

  If a project does not exist, the metadata is None.

  The project metadata stored in project.cfg files in each project.
  """
  return _get_project_configs(
      project_ids, common.PROJECT_METADATA_FILENAME,
      project_config_pb2.ProjectCfg)


def get_refs(project_ids):
  """Returns a mapping {project_id: list of refs}

  The ref list is None if a project does not exist.

  The list of refs stored in refs.cfg of a project.
  """
  cfgs = _get_project_configs(
      project_ids, common.REFS_FILENAME, project_config_pb2.RefsCfg)
  return {
    pid: None if cfg is None else cfg.refs or DEFAULT_REF_CFG.refs
    for pid, cfg in cfgs.iteritems()
  }


def _get_project_configs(project_ids, path, message_factory):
  """Returns a mapping {project_id: message}.

  If a project does not exist, the message is None.
  """
  assert isinstance(project_ids, list)
  if not project_ids:
    return {}
  prefix = 'projects/'
  messages = storage.get_latest_messages_async(
      [prefix + pid for pid in _filter_existing(project_ids)],
      path, message_factory).get_result()
  return {
    # messages may not have a key because we filter project ids by existence
    pid: messages.get(prefix + pid)
    for pid in project_ids
  }


def _filter_existing(project_ids):
  # TODO(nodir): optimize
  assert isinstance(project_ids, list)
  if not project_ids:
    return project_ids
  assert all(pid for pid in project_ids)
  all_project_ids = set(p.id for p in get_projects())
  return [
    pid for pid in project_ids
    if pid in all_project_ids
  ]