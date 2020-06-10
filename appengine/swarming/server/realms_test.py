#!/usr/bin/env vpython
# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import logging
import sys
import unittest

import mock
from parameterized import parameterized

import test_env
test_env.setup_test_env()

import endpoints

from components import auth
from components import utils
from test_support import test_case

from proto.config import config_pb2
from proto.config import pools_pb2
from proto.config import realms_pb2
from server import config
from server import pools_config
from server import realms
from server import service_accounts
from server import task_request
from server import task_scheduler


_PERM_POOLS_CREATE_TASK = auth.Permission('swarming.pools.createTask')
_PERM_TASKS_CREATE_IN_REALM = auth.Permission('swarming.tasks.createInRealm')
_PERM_TASKS_RUN_AS = auth.Permission('swarming.tasks.runAs')
_TASK_SERVICE_ACCOUNT_IDENTITY = auth.Identity(
    auth.IDENTITY_USER, 'test@test-service-accounts.iam.gserviceaccount.com')


def _gen_task_request_mock(realm='test:realm'):
  mocked = mock.create_autospec(
      task_request.TaskRequest, spec_set=True, instance=True)
  mocked.max_lifetime_secs = 1
  mocked.service_account = _TASK_SERVICE_ACCOUNT_IDENTITY.name
  mocked.realm = realm
  return mocked


def _gen_pool_config(realm='test:pool/realm',
                     dry_run_task_realm='test:realm_dryrun',
                     enforced_realm_permissions=()):
  return pools_config.init_pool_config(
      name='default',
      rev='pools_cfg_rev',
      realm=realm,
      enforced_realm_permissions=frozenset(enforced_realm_permissions),
      dry_run_task_realm=dry_run_task_realm)


class RealmsTest(test_case.TestCase):

  def setUp(self):
    super(RealmsTest, self).setUp()
    self._has_permission_mock = mock.Mock()
    self._has_permission_dryrun_mock = mock.Mock()
    self.mock(auth, 'has_permission', self._has_permission_mock)
    self.mock(auth, 'has_permission_dryrun', self._has_permission_dryrun_mock)
    self.mock(service_accounts, 'has_token_server', lambda: True)
    utils.clear_cache(config.settings)

  def tearDown(self):
    super(RealmsTest, self).tearDown()
    utils.clear_cache(config.settings)

  def test_get_permission(self):
    perm = realms.get_permission(realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK)
    self.assertEqual(_PERM_POOLS_CREATE_TASK, perm)

  def test_has_permission_wrapper(self):
    perm = realms.get_permission(realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK)
    self._has_permission_mock.side_effect = ValueError('Invalid realm.')
    with self.assertRaises(auth.AuthorizationError):
      realms._has_permission(perm, ['invalid'])

  @parameterized.expand([
      # should return False if the permissiion is not configured in settings.cfg
      # and in pools.cfg.
      (
          False,
          config_pb2.SettingsCfg(),
          _gen_pool_config(),
      ),
      # should return True if the permission is enforced in the pool.
      (True, config_pb2.SettingsCfg(),
       _gen_pool_config(enforced_realm_permissions=[
           realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK
       ])),
      # return True if the permission is enforced globally.
      (True,
       config_pb2.SettingsCfg(
           auth=config_pb2.AuthSettings(enforced_realm_permissions=[
               realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK
           ])), _gen_pool_config()),
  ])
  def test_is_enforced_permission(self, expected, settings_cfg, pool_cfg):
    self.mock(config, '_get_settings', lambda: (None, settings_cfg))
    self.assertEqual(expected, realms.is_enforced_permission(
        realms_pb2.REALM_PERMISSION_POOLS_CREATE_TASK, pool_cfg))

  def _mock_for_check_pools_create_task_legacy(self, is_allowed_legacy):
    self.mock(realms, 'is_enforced_permission', lambda *_: False)
    self.mock(task_scheduler,
              '_is_allowed_to_schedule', lambda _: is_allowed_legacy)

  def _mock_for_check_pools_create_task(self, pool_realm='test:pool'):
    self.mock(realms, 'is_enforced_permission', lambda *_: True)
    self.mock(pools_config,
              'get_pool_config', lambda _: _gen_pool_config(realm=pool_realm))

  def test_check_pools_create_task_legacy_allowed(self):
    self._mock_for_check_pools_create_task_legacy(is_allowed_legacy=True)
    realms.check_pools_create_task('test_pool',
                                   _gen_pool_config(realm='test:pool'))
    self._has_permission_dryrun_mock.assert_called_once_with(
        _PERM_POOLS_CREATE_TASK, [u'test:pool'],
        True,
        tracking_bug='crbug.com/1066839')

  def test_check_pools_create_task_legacy_allowed_no_pool_realm(self):
    self._mock_for_check_pools_create_task_legacy(is_allowed_legacy=True)
    realms.check_pools_create_task('test_pool', _gen_pool_config(realm=None))
    self._has_permission_dryrun_mock.assert_not_called()

  def test_check_pools_create_task_legacy_not_allowed(self):
    self._mock_for_check_pools_create_task_legacy(is_allowed_legacy=False)
    with self.assertRaises(auth.AuthorizationError):
      realms.check_pools_create_task('test_pool',
                                     _gen_pool_config(realm='test:pool'))
    self._has_permission_dryrun_mock.assert_called_once_with(
        _PERM_POOLS_CREATE_TASK, [u'test:pool'],
        False,
        tracking_bug='crbug.com/1066839')

  def test_check_pools_create_task_legacy_not_allowed_no_pool_realm(self):
    self._mock_for_check_pools_create_task_legacy(is_allowed_legacy=False)
    with self.assertRaises(auth.AuthorizationError):
      realms.check_pools_create_task('test_pool', _gen_pool_config(realm=None))
    self._has_permission_dryrun_mock.assert_not_called()

  def test_check_pools_create_task_enforced_allowed(self):
    self._mock_for_check_pools_create_task()
    self._has_permission_mock.return_value = True
    realms.check_pools_create_task('test_pool',
                                   _gen_pool_config(realm='test:pool'))
    self._has_permission_mock.assert_called_once_with(_PERM_POOLS_CREATE_TASK,
                                                      [u'test:pool'], identity=None)

  def test_check_pools_create_task_enforced_not_allowed(self):
    self._mock_for_check_pools_create_task()
    self._has_permission_mock.return_value = False
    with self.assertRaises(auth.AuthorizationError):
      realms.check_pools_create_task('test_pool',
                                     _gen_pool_config(realm='test:pool'))
    self._has_permission_mock.assert_called_once_with(_PERM_POOLS_CREATE_TASK,
                                                      [u'test:pool'], identity=None)

  def test_check_tasks_create_in_realm_legacy(self):
    pool_cfg_mock = _gen_pool_config()
    realms.check_tasks_create_in_realm(None, pool_cfg_mock)
    self._has_permission_dryrun_mock.assert_called_once_with(
        _PERM_TASKS_CREATE_IN_REALM, [u'test:realm_dryrun'],
        expected_result=True,
        tracking_bug=realms._TRACKING_BUG)

  def test_check_tasks_create_in_realm_legacy_no_dryrun_realm(self):
    pool_cfg_mock = _gen_pool_config(dry_run_task_realm=None)
    realms.check_tasks_create_in_realm(None, pool_cfg_mock)
    self._has_permission_dryrun_mock.assert_not_called()

  def test_check_tasks_create_in_realm_enforced_allowed(self):
    self._has_permission_mock.return_value = True
    pool_cfg_mock = _gen_pool_config()
    realms.check_tasks_create_in_realm('test:realm', pool_cfg_mock)
    self._has_permission_mock.assert_called_once_with(
        _PERM_TASKS_CREATE_IN_REALM, [u'test:realm'], identity=None)

  def test_check_tasks_create_in_realm_enforced_not_allowed(self):
    self._has_permission_mock.return_value = False
    pool_cfg_mock = _gen_pool_config()
    with self.assertRaises(auth.AuthorizationError):
      realms.check_tasks_create_in_realm('test:realm', pool_cfg_mock)
    self._has_permission_mock.assert_called_once_with(
        _PERM_TASKS_CREATE_IN_REALM, [u'test:realm'], identity=None)

  def test_check_tasks_create_in_realm_enforced_no_realm(self):
    pool_cfg_mock = _gen_pool_config(enforced_realm_permissions=[
        realms_pb2.REALM_PERMISSION_TASKS_CREATE_IN_REALM
    ])
    with self.assertRaises(auth.AuthorizationError):
      realms.check_tasks_create_in_realm(None, pool_cfg_mock)

  def test_check_tasks_run_as_legacy_allowed(self):
    self.mock(task_scheduler, '_is_allowed_service_account', lambda *_: True)
    task_request_mock = _gen_task_request_mock(realm=None)
    pool_cfg_mock = _gen_pool_config()
    realms.check_tasks_run_as(task_request_mock, pool_cfg_mock)
    self._has_permission_dryrun_mock.assert_called_once_with(
        _PERM_TASKS_RUN_AS, [u'test:realm_dryrun'],
        True,
        identity=_TASK_SERVICE_ACCOUNT_IDENTITY,
        tracking_bug=realms._TRACKING_BUG)

  def test_check_tasks_run_as_legacy_not_allowed(self):
    self.mock(task_scheduler, '_is_allowed_service_account', lambda *_: False)
    task_request_mock = _gen_task_request_mock(realm=None)
    pool_cfg_mock = _gen_pool_config()
    with self.assertRaises(auth.AuthorizationError):
      realms.check_tasks_run_as(task_request_mock, pool_cfg_mock)
    self._has_permission_dryrun_mock.assert_called_once_with(
        _PERM_TASKS_RUN_AS, [u'test:realm_dryrun'],
        False,
        identity=_TASK_SERVICE_ACCOUNT_IDENTITY,
        tracking_bug=realms._TRACKING_BUG)

  def test_check_tasks_run_as_enforced_allowed(self):
    self._has_permission_mock.return_value = True
    task_request_mock = _gen_task_request_mock()
    pool_cfg_mock = _gen_pool_config()
    realms.check_tasks_run_as(task_request_mock, pool_cfg_mock)
    self._has_permission_mock.assert_called_once_with(
        _PERM_TASKS_RUN_AS, [u'test:realm'],
        identity=_TASK_SERVICE_ACCOUNT_IDENTITY)

  def test_check_tasks_run_as_enforced_no_realm(self):
    self._has_permission_mock.return_value = False
    task_request_mock = _gen_task_request_mock(realm=None)
    pool_cfg_mock = _gen_pool_config(
        enforced_realm_permissions=[realms_pb2.REALM_PERMISSION_TASKS_RUN_AS])
    with self.assertRaises(auth.AuthorizationError):
      realms.check_tasks_run_as(task_request_mock, pool_cfg_mock)
    self._has_permission_mock.assert_not_called()

  def test_check_tasks_run_as_enforced_not_allowed(self):
    self.mock(realms, 'is_enforced_permission', lambda *_: True)
    self._has_permission_mock.return_value = False
    task_request_mock = _gen_task_request_mock()
    pool_cfg_mock = _gen_pool_config()
    with self.assertRaises(auth.AuthorizationError):
      realms.check_tasks_run_as(task_request_mock, pool_cfg_mock)
    self._has_permission_mock.assert_called_once_with(
        _PERM_TASKS_RUN_AS, [u'test:realm'],
        identity=_TASK_SERVICE_ACCOUNT_IDENTITY)


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  logging.basicConfig(
      level=logging.DEBUG if '-v' in sys.argv else logging.CRITICAL)
  unittest.main()
