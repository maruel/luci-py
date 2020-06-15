# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import datetime
import logging

from components import auth

from proto.config import realms_pb2
from server import config
from server import task_scheduler

_TRACKING_BUG = 'crbug.com/1066839'


def get_permission(enum_permission):
  """ Generates Realm permission instance from enum value.

  e.g. realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK
       -> 'swarming.pools.createTask'

  Args:
    enum_permission: realms_pb2.RealmPermission enum value.

  Returns:
    realm_permission: an instance of auth.Permission.
  """
  enum_name = realms_pb2.RealmPermission.Name(enum_permission)
  words = enum_name.replace('REALM_PERMISSION_', '').split('_')
  # convert first word to subject e.g. pools, tasks
  subject = words[0].lower()
  # convert following words to verb e.g. createTask, listBots
  verb = words[1].lower() + ''.join(map(lambda x: x.capitalize(), words[2:]))
  return auth.Permission('swarming.%s.%s' % (subject, verb))


def is_enforced_permission(perm, pool_cfg=None):
  """ Checks if the Realm permission is enforced.

  Checks if the permission is specified in `enforced_realm_permissions`
  in settings.cfg or pools.cfg for the pool.

  Args:
    perm: realms_pb2.RealmPermission enum value.
    pool_cfg: PoolConfig of the pool

  Returns:
    bool: True if it's enforced, False if it's legacy-compatible.
  """
  if pool_cfg and perm in pool_cfg.enforced_realm_permissions:
    return True
  return perm in config.settings().auth.enforced_realm_permissions


def check_pools_create_task(pool, pool_cfg):
  """Checks if the caller can create the task in the pool.

  Realm permission `swarming.pools.createTask` will be checked,
  using auth.has_permission() or auth.has_permission_dryrun().

  If the realm permission check is enforced,
    It just calls auth.has_permission()

  If it's legacy-compatible,
    It calls the legacy task_scheduler._is_allowed_to_schedule() and compare
    the legacy result with the realm permission check using the dryrun.

  Args:
    pool: Pool in which the caller is scheduling a new task.
    pool_cfg: PoolCfg of the pool.

  Returns:
    None

  Raises:
    auth.AuthorizationError: if the caller is not allowed to schedule the task
                             in the pool.
  """
  perm = realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK

  legacy_err_msg = (
      'User "%s" is not allowed to schedule tasks in the pool "%s", '
      'see pools.cfg' % (auth.get_current_identity().to_bytes(), pool))

  def check_auth_legacy():
    return task_scheduler._is_allowed_to_schedule(pool_cfg)

  _check_permission(
      perm,
      pool_cfg.realm,
      is_enforced=is_enforced_permission(perm, pool_cfg),
      legacy_check_func=check_auth_legacy,
      legacy_auth_err_msg=legacy_err_msg,
      dryrun_realm=pool_cfg.realm)


def check_tasks_create_in_realm(realm, pool_cfg):
  """Checks if the caller is allowed to create a task in the realm.

  Args:
    realm: Realm that a task will be created in.
    pool_cfg: PoolConfig of the pool where the task will run.

  Returns:
    None

  Raises:
    auth.AuthorizationError: if the caller is not allowed.
  """
  perm = realms_pb2.REALM_PERMISSION_TASKS_CREATE_IN_REALM
  _check_permission(
      perm,
      realm,
      is_enforced=bool(realm) or is_enforced_permission(perm, pool_cfg),
      dryrun_realm=realm or pool_cfg.dry_run_task_realm)


def check_tasks_run_as(task_request, pool_cfg):
  """Checks if the task service account is allowed to run in the task realm.

  Realm permission `swarming.tasks.runAs` will be checked,
  using auth.has_permission() or auth.has_permission_dryrun().

  If the realm permission check is enforced,
    It just calls auth.has_permission()

  If it's legacy-compatible,
    It calls task_scheduler._is_allowed_service_account() and compare the
    legacy result with the realm permission check using the dryrun.

  Args:
    task_request: TaskRequest entity to be scheduled.
    pool_cfg: PoolConfig of the pool where the task will run.

  Returns:
    None

  Raises:
    auth.AuthorizationError: if the service account is not allowed to run
                             in the task realm.
  """
  perm = realms_pb2.REALM_PERMISSION_TASKS_RUN_AS

  # Enforce if the requested task has realm or it's configured in pools.cfg or
  # in settings.cfg globally.
  is_enforced = (
      bool(task_request.realm) or is_enforced_permission(perm, pool_cfg))

  def check_auth_legacy():
    return task_scheduler._is_allowed_service_account(
        task_request.service_account, pool_cfg)

  err_msg = (
      'Task service account "%s" as specified in the task request is not '
      'allowed to be used in the pool "%s". Is allowed_service_account or '
      'allowed_service_account_group specified in pools.cfg?' %
      (task_request.service_account, task_request.pool))

  dryrun_realm = task_request.realm or pool_cfg.dry_run_task_realm

  _check_permission(
      perm,
      task_request.realm,
      identity=auth.Identity(auth.IDENTITY_USER, task_request.service_account),
      is_enforced=is_enforced,
      legacy_check_func=check_auth_legacy,
      legacy_auth_err_msg=err_msg,
      dryrun_realm=dryrun_realm)


def _check_permission(enum_permission,
                      realm,
                      identity=None,
                      is_enforced=False,
                      legacy_check_func=lambda: True,
                      legacy_auth_err_msg=None,
                      dryrun_realm=None):
  """Checks if the caller has the permission.

  If the realm permission check is enforced,
   It just calls auth.has_permission()

  If it's legacy-compatible,
   It calls the legacy permission check function, and compare the legacy result
   with the realm check result using auth.has_permission_dryrun().

  Args:
    enum_permission: realms_pb2.RealmPermission enum value.
    realm: name of the Realm.
    identity: an instance of auth.Identity to check permission.
              default is auth.get_current_identity().
    is_enforced: boolean with the enforcement of Realm permission check.
    legacy_check_func: a function to check permission. required if not enforced.
    legach_auth_err_msg: auth.AuthorizationError message for legacy path.

  Returns:
    None

  Raises:
    auth.AuthorizationError: if the caller is not allowed.
  """
  if not identity:
    identity = auth.get_current_identity()
  perm = get_permission(enum_permission)

  if is_enforced:
    if not realm:
      raise auth.AuthorizationError('Realm is missing')

    if not auth.has_permission(perm, [realm], identity=identity):
      raise auth.AuthorizationError(
          '[realms] Identity "%s" does not have permission "%s" in realm "%s"' %
          (identity, perm.name, realm))
    logging.info('[realms] Identity "%s" has permission "%s" in realm "%s"',
                 identity, perm.name, realm)
    return

  # legacy path
  legacy_allowed = legacy_check_func()

  if dryrun_realm:
    auth.has_permission_dryrun(
        perm, [dryrun_realm],
        legacy_allowed,
        identity=identity,
        tracking_bug=_TRACKING_BUG)

  if not legacy_allowed:
    raise auth.AuthorizationError(legacy_auth_err_msg)
