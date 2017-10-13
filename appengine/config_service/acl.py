# Copyright 2015 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

from components import auth
from components import config
from components import utils
from components.config.proto import service_config_pb2

import common
import projects
import services
import storage


# Cache acl.cfg for 10min. It never changes.
@utils.cache_with_expiration(10 * 60)
def get_acl_cfg():
  return storage.get_self_config_async(
      common.ACL_FILENAME, service_config_pb2.AclCfg).get_result()


def can_read_config_sets(config_sets):
  """Returns a mapping {config_set: has_access}.

  has_access is True if current requester has access to the config set.

  Raise:
    ValueError if any config_set is malformed.
  """
  assert isinstance(config_sets, list)
  check_via = {}
  for cs in config_sets:
    ref_match = config.REF_CONFIG_SET_RGX.match(cs)
    if ref_match:
      project_id = ref_match.group(1)
      check_via[cs] = 'projects/' + project_id
    else:
      check_via[cs] = cs

  project_ids = []
  service_ids = []
  for cs in set(check_via.itervalues()):
    service_match = config.SERVICE_CONFIG_SET_RGX.match(cs)
    if service_match:
      service_ids.append(service_match.group(1))
    else:
      project_match = config.PROJECT_CONFIG_SET_RGX.match(cs)
      if project_match:
        project_ids.append(project_match.group(1))
      else:
        raise ValueError('invalid config_set %r' % cs)

  access_map = {}
  for pid, access in has_projects_access(project_ids).iteritems():
    access_map['projects/' + pid] = access
  for sid, access in has_services_access(service_ids).iteritems():
    access_map['services/' + sid] = access

  return {
    cs: access_map[check_via[cs]]
    for cs in config_sets
  }


def is_admin():
  if auth.is_superuser():
    return True
  acl_cfg = get_acl_cfg()
  return auth.is_group_member(
      acl_cfg and acl_cfg.admin_group or auth.ADMIN_GROUP)


def has_services_access(service_ids):
  """Returns a mapping {service_id: has_access}.

  has_access is True if current requester can read service configs.
  """
  assert isinstance(service_ids, list)
  if not service_ids:
    return {}
  for sid in service_ids:
    assert isinstance(sid, basestring)
    assert sid

  if is_admin():
    return {sid: True for sid in service_ids}

  cfgs = {
    s.id: s
    for s in services.get_services_async().get_result()
  }

  def acc_list(sid):
    cfg = cfgs.get(sid)
    if not cfg:
      return []
    ret = cfg.access
    for o in cfg.owners:
      ret.append('user:%s' % o)
    return ret

  return _has_access({
    sid: acc_list(sid)
    for sid in set(service_ids)
  })


def has_projects_access(project_ids):
  if not project_ids:
    return {}
  super_group = get_acl_cfg().project_access_group
  if is_admin() or super_group and auth.is_group_member(super_group):
    return {pid: True for pid in project_ids}
  metadata = projects.get_metadata_async(project_ids).get_result()

  def acc_list(pid):
    md = metadata.get(pid)
    return md.access if md else []

  return _has_access({
    pid: acc_list(pid)
    for pid in set(project_ids)
  })


def _has_access(resources):
  access_values = set()
  for acc_list in resources.itervalues():
    access_values.update(acc_list)

  has_access = {
    a: config.api._has_access(a)
    for a in access_values
  }
  return {
    id: any(has_access[a] for a in acc_list)
    for id, acc_list in resources.iteritems()
  }
