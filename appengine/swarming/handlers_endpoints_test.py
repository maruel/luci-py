#!/usr/bin/env python
# coding=utf-8
# Copyright 2015 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import base64
import datetime
import json
import logging
import os
import random
import sys
import unittest

import test_env_handlers
from test_support import test_case

from google.appengine.ext import ndb
from protorpc.remote import protojson
import webapp2
import webtest

from components import auth
from components import ereporter2
from components import utils

import handlers_bot
import handlers_endpoints
import swarming_rpcs

from server import acl
from server import bot_code
from server import bot_management
from server import config
from server import large
from server import task_pack
from server import task_queues
from server import task_request
from server import task_result


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
DATETIME_NO_MICRO = '%Y-%m-%dT%H:%M:%S'


def message_to_dict(rpc_message):
  return json.loads(protojson.encode_message(rpc_message))


class BaseTest(test_env_handlers.AppTestBase, test_case.EndpointsTestCase):
  def setUp(self):
    test_case.EndpointsTestCase.setUp(self)
    super(BaseTest, self).setUp()
    # handlers_bot is necessary to create fake tasks.
    self.app = webtest.TestApp(
        webapp2.WSGIApplication(handlers_bot.get_routes(), debug=True),
        extra_environ={
          'REMOTE_ADDR': self.source_ip,
          'SERVER_SOFTWARE': os.environ['SERVER_SOFTWARE'],
        })
    self.mock(
        ereporter2, 'log_request',
        lambda *args, **kwargs: self.fail('%s, %s' % (args, kwargs)))
    # Client API test cases run by default as user.
    self.set_as_user()
    self.mock(utils, 'enqueue_task', self._enqueue_task)
    self.now = datetime.datetime(2010, 1, 2, 3, 4, 5)
    self.mock_now(self.now)

  @ndb.non_transactional
  def _enqueue_task(self, url, queue_name, **kwargs):
    if queue_name == 'rebuild-task-cache':
      # Call directly into it.
      self.assertEqual(True, task_queues.rebuild_task_cache(kwargs['payload']))
      return True
    if queue_name == 'pubsub':
      return True
    self.fail(url)


class ServerApiTest(BaseTest):
  api_service_cls = handlers_endpoints.SwarmingServerService

  def test_details(self):
    """Asserts that server_details returns the correct version."""
    self.mock(config.config, 'config_service_hostname', lambda: 'a.server')

    cfg = config.settings()
    cfg.isolate.default_server = 'https://isolateserver.appspot.com'
    cfg.isolate.default_namespace = 'default-gzip'
    self.mock(config, 'settings', lambda: cfg)

    response = self.call_api('details')
    expected = {
      u'bot_version': unicode(
          bot_code.get_bot_version('https://testbed.example.com')[0]),
      u'display_server_url_template': u'',
      u'luci_config': u'a.server',
      u'default_isolate_server': u'https://isolateserver.appspot.com',
      u'default_isolate_namespace': u'default-gzip',
      u'machine_provider_template':
          u'https://machine-provider.appspot.com/leases/%s',
      u'server_version': unicode(utils.get_app_version()),
    }
    self.assertEqual(expected, response.json)

  def test_public_permissions(self):
    """Asserts that permissions respond correctly to an unauthed user."""
    self.set_as_anonymous()
    response = self.call_api('permissions')
    expected = {
        u'cancel_task': False,
        u'cancel_tasks': False,
        u'delete_bot': False,
        u'get_bootstrap_token': False,
        u'get_configs': False,
        u'put_configs': False,
        u'terminate_bot': False,
    }
    self.assertEqual(expected, response.json)

  def test_user_permissions(self):
    """Asserts that permissions respond correctly to a basic user."""
    self.set_as_user()
    response = self.call_api('permissions')
    expected = {
        u'cancel_task': True,
        u'cancel_tasks': False,
        u'delete_bot': False,
        u'get_bootstrap_token': False,
        u'get_configs': False,
        u'put_configs': False,
        u'terminate_bot': False,
    }
    self.assertEqual(expected, response.json)

  def test_privileged_user_permissions(self):
    """Asserts that permissions respond correctly to a privileged user."""
    self.set_as_privileged_user()
    response = self.call_api('permissions')
    expected = {
        u'cancel_task': True,
        u'cancel_tasks': False,
        u'delete_bot': False,
        u'get_bootstrap_token': False,
        u'get_configs': False,
        u'put_configs': False,
        u'terminate_bot': True,
    }
    self.assertEqual(expected, response.json)

  def test_admin_permissions(self):
    """Asserts that permissions respond correctly to an admin."""
    self.set_as_admin()
    response = self.call_api('permissions')
    expected = {
        u'cancel_task': True,
        u'cancel_tasks': True,
        u'delete_bot': True,
        u'get_bootstrap_token': True,
        u'get_configs': True,
        u'put_configs': True,
        u'terminate_bot': True,
    }
    self.assertEqual(expected, response.json)

  def _test_file(self, name, header):
    # Tests either get_bootstrap or get_bot_config.
    self.set_as_admin()
    path = os.path.join(self.APP_DIR, 'swarming_bot', 'config', name + '.py')
    with open(path, 'rb') as f:
      content = f.read().decode('utf-8')

    expected = {
      u'content': header + content,
    }
    self.assertEqual(expected, self.call_api('get_' + name).json)

    # Define a script on the luci-config server.
    def get_self_config_mock(path, revision=None, store_last_good=False):
      self.assertEqual('scripts/%s.py' % name, path)
      if revision:
        self.assertEqual(False, store_last_good)
        return revision, 'old code'
      self.assertEqual(None, revision)
      self.assertEqual(True, store_last_good)
      return 'abc', 'foo bar'
    def config_service_hostname_mock():
      return 'localhost:1'
    self.mock(bot_code.config, 'get_self_config', get_self_config_mock)
    self.mock(
        bot_code.config, 'config_service_hostname',
        config_service_hostname_mock)

    expected = {
      u'content': header + u'foo bar',
      u'version': u'abc',
      u'who': u'localhost:1',
    }
    self.assertEqual(expected, self.call_api('get_' + name).json)

  def test_bootstrap(self):
    self._test_file(
        'bootstrap',
        '#!/usr/bin/env python\n'
        '# coding: utf-8\n'
        'host_url = \'\'\n'
        'bootstrap_token = \'\'\n')

  def test_bot_config(self):
    self._test_file('bot_config', '')


class TasksApiTest(BaseTest):
  api_service_cls = handlers_endpoints.SwarmingTasksService

  def setUp(self):
    super(TasksApiTest, self).setUp()
    utils.clear_cache(config.settings)
    self.mock_default_pool_acl(['service-account@example.com'])

  def test_new_ok_raw(self):
    """Asserts that new generates appropriate metadata."""
    oauth_grant_calls = self.mock_task_service_accounts()
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))

    request = self.create_new_request(
        expiration_secs=30,
        properties=self.create_props(
            command=['rm', '-rf', '/'],
            execution_timeout_secs=30,
            grace_period_secs=15),
        pubsub_topic='projects/abc/topics/def',
        pubsub_auth_token='secret that must not be shown',
        pubsub_userdata='userdata',
        service_account='service-account@example.com')
    expected = {
      u'request': self.gen_request(
        created_ts=str_now,
        expiration_secs=u'30',
        priority=u'20',
        properties=self.gen_props(
            command=[u'rm', u'-rf', u'/'],
            execution_timeout_secs=u'30',
            grace_period_secs=u'15'),
        pubsub_topic=u'projects/abc/topics/def',
        pubsub_userdata=u'userdata',
        tags=[
          u'a:tag',
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'service_account:service-account@example.com',
          u'user:joe@localhost'
        ],
        service_account='service-account@example.com',
        task_slices=[
          {
            u'expiration_secs': u'30',
            u'properties': expected_properties,
          },
        ]),
      u'task_id': u'5cee488008810',
    }

    response = self.call_api('new', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

    # Asked for a correct grant.
    self.assertEqual(
        [(u'service-account@example.com', datetime.timedelta(0, 30+30+15))],
        oauth_grant_calls)

  def test_new_bad_service_account(self):
    oauth_grant_calls = self.mock_task_service_accounts()
    request = self.create_new_request(
        properties=self.create_props(command=['rm', '-rf', '/']),
        service_account='bad email')
    response = self.call_api('new', body=message_to_dict(request), status=400)
    # Note: Cloud Endpoints proxy transform this response to
    # {"error": {"message": "..."}}.
    self.assertEqual({
        u'error_message': u'\'service_account\' must be an email, "bot" or '
            '"none" string, got u\'bad email\'',
        u'state': u'APPLICATION_ERROR',
    }, response.json)
    self.assertFalse(oauth_grant_calls)

  def test_new_forbidden_service_account(self):
    self.mock_task_service_accounts(
        exc=auth.AuthorizationError('forbidden account'))
    request = self.create_new_request(
        properties=self.create_props(command=['rm', '-rf', '/']),
        service_account='service-account@example.com')
    response = self.call_api('new', body=message_to_dict(request), status=403)
    # Note: Cloud Endpoints proxy transform this response to
    # {"error": {"message": "..."}}.
    self.assertEqual({
        u'error_message': u'forbidden account',
        u'state': u'APPLICATION_ERROR',
    }, response.json)

  def test_new_ok_deduped(self):
    """Asserts that new returns task result for deduped."""
    # Run a task to completion.
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    self.client_create_task_raw(
        tags=['project:yay', 'commit:post'],
        properties=dict(idempotent=True))
    self.set_as_bot()
    self.bot_run_task()

    self.mock(random, 'getrandbits', lambda _: 0x66)
    now_30 = self.mock_now(self.now, 30)
    str_now_30 = unicode(now_30.strftime(DATETIME_NO_MICRO))

    # Expectations.
    t_result = self.gen_result_summary(
        completed_ts=str_now,
        costs_usd=[0.1],
        created_ts=str_now,
        duration=0.1,
        exit_code=u'0',
        modified_ts=str_now,
        started_ts=str_now,
        tags=[
          u'commit:post',
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'project:yay',
          u'service_account:none',
          u'user:joe@localhost',
        ],
        try_number=u'1')
    t_request = self.gen_request(
        created_ts=str_now,
        properties=self.gen_props(
            command=[u'python', u'run_test.py'], idempotent=True),
        priority=u'20',
        tags=[
          u'commit:post',
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'project:yay',
          u'service_account:none',
          u'user:joe@localhost',
        ])

    # Make sure it completed.
    self.set_as_privileged_user()
    expected = {u'items': [t_result], u'now': str_now_30}
    response = self.call_api(
        'list', body=message_to_dict(swarming_rpcs.TasksRequest()))
    self.assertEqual(expected, response.json)
    expected = {u'items': [t_request], u'now': str_now_30}
    response = self.call_api(
        'requests', body=message_to_dict(swarming_rpcs.TasksRequest()))
    self.assertEqual(expected, response.json)

    # Expectations.
    deduped_props = self.gen_props(
        command=[u'python', u'run_test.py'], idempotent=True)
    deduped_request = self.gen_request(
        created_ts=str_now_30,
        expiration_secs=u'30',
        name=u'job2',
        priority=u'200',
        tags=[
          u'commit:pre',
          u'os:Amiga',
          u'pool:default',
          u'priority:200',
          u'service_account:none',
          u'user:joe@localhost',
        ],
        task_slices=[
          {
            u'expiration_secs': u'30',
            u'properties': deduped_props,
          },
        ],
        properties=deduped_props)
    deduped_result = self.gen_result_summary(
        completed_ts=str_now,
        cost_saved_usd=0.1,
        created_ts=str_now_30,
        duration=0.1,
        deduped_from=u'5cee488008811',
        exit_code=u'0',
        modified_ts=str_now_30,
        name=u'job2',
        task_id=u'5cf59b8006610',
        started_ts=str_now,
        tags=[
          u'os:Amiga',
          u'pool:default',
          u'priority:200',
          u'service_account:none',
          u'user:joe@localhost',
        ])

    expected = {
      u'request': deduped_request,
      u'task_id': u'5cf59b8006610',
      u'task_result': deduped_result,
    }
    self.set_as_user()
    new_req = self.create_new_request(
        expiration_secs=30,
        name='job2',
        priority=200,
        tags=['commit:pre'],
        properties=self.create_props(
            command=['python', 'run_test.py'], idempotent=True))
    response = self.call_api('new', body=message_to_dict(new_req))
    self.assertEqual(expected, response.json)

    self.set_as_privileged_user()
    expected = {
      u'items': [deduped_result],
      u'now': str_now_30,
    }
    response = self.call_api(
        'list',
        body=message_to_dict(
            swarming_rpcs.TasksRequest(state=swarming_rpcs.TaskState.DEDUPED)))
    self.assertEqual(expected, response.json)

    # Assert the entity presence.
    self.assertEqual(2, task_request.TaskRequest.query().count())
    self.assertEqual(2, task_result.TaskResultSummary.query().count())
    self.assertEqual(1, task_result.TaskRunResult.query().count())

    # Deduped task have no performance data associated.
    response = self.call_api(
        'list',
        body=message_to_dict(
            swarming_rpcs.TasksRequest(
                state=swarming_rpcs.TaskState.DEDUPED,
                include_performance_stats=True)))
    self.assertEqual(expected, response.json)

    # Use the occasion to test 'count' and 'requests'.
    start = utils.datetime_to_timestamp(self.now) / 1000000. - 1
    end = utils.datetime_to_timestamp(now_30) / 1000000. + 1
    response = self.call_api(
        'count',
        body=message_to_dict(
            swarming_rpcs.TasksCountRequest(
                start=start, end=end, state=swarming_rpcs.TaskState.DEDUPED)))
    self.assertEqual({u'now': str_now_30, u'count': u'1'}, response.json)

    expected = {u'items': [deduped_request, t_request], u'now': str_now_30}
    response = self.call_api(
        'requests',
        body=message_to_dict(
            swarming_rpcs.TasksRequest(start=start, end=end)))
    self.assertEqual(expected, response.json)

  def test_new_ok_isolated(self):
    """Asserts that new generates appropriate metadata."""
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    request = self.create_new_request(
        properties=self.create_props(
            inputs_ref=swarming_rpcs.FilesRef(
                isolated='1'*40,
                isolatedserver='http://localhost:1',
                namespace='default-gzip')))
    expected = {
      u'request': self.gen_request(
          created_ts=str_now,
          properties=self.gen_props(
              inputs_ref={
                u'isolated': u'1'*40,
                u'isolatedserver': u'http://localhost:1',
                u'namespace': u'default-gzip',
              })),
      u'task_id': u'5cee488008810',
    }
    response = self.call_api('new', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

  def test_new_ok_isolated_with_defaults(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))

    cfg = config.settings()
    cfg.isolate.default_server = 'https://isolateserver.appspot.com'
    cfg.isolate.default_namespace = 'default-gzip'
    self.mock(config, 'settings', lambda: cfg)

    request = self.create_new_request(
        properties=self.create_props(
            inputs_ref=swarming_rpcs.FilesRef(isolated='1'*40)))
    expected_props = self.gen_props(
        inputs_ref={
          u'isolated': u'1'*40,
          u'isolatedserver': u'https://isolateserver.appspot.com',
          u'namespace': u'default-gzip',
        })
    expected = {
      u'request': self.gen_request(
          created_ts=str_now,
          properties=expected_props,
          task_slices=[
            {
              u'expiration_secs': u'86400',
              u'properties': expected_props,
            },
          ]),
      u'task_id': u'5cee488008810',
    }
    response = self.call_api('new', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

  def test_new_cipd_package_with_defaults(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))

    # Define settings on the server.
    cfg = config.settings()
    cfg.cipd.default_client_package.package_name = (
        'infra/tools/cipd/${platform}')
    cfg.cipd.default_client_package.version = 'git_revision:deadbeef'
    cfg.cipd.default_server = 'https://chrome-infra-packages.appspot.com'
    self.mock(config, 'settings', lambda: cfg)

    expected = {
      u'request': self.gen_request(
          created_ts=str_now,
          properties=self.gen_props(
              cipd_input={
                u'client_package': {
                  u'package_name': u'infra/tools/cipd/${platform}',
                  u'version': u'git_revision:deadbeef',
                },
                u'packages': [
                  {
                    u'package_name': u'rm',
                    u'path': u'.',
                    u'version': u'latest',
                  },
                ],
                u'server': u'https://chrome-infra-packages.appspot.com',
              },
              command=[u'rm', u'-rf', u'/'],
              env=[{u'key': u'PATH', u'value': u'/'}])),
      u'task_id': u'5cee488008810',
    }
    request = self.create_new_request(
        properties=self.create_props(
            cipd_input=swarming_rpcs.CipdInput(
                packages=[
                  swarming_rpcs.CipdPackage(
                      package_name='rm', path='.', version='latest'),
                ]),
            command=['rm', '-rf', '/'],
            env=[
              swarming_rpcs.StringPair(key='PATH', value='/'),
            ]))
    response = self.call_api('new', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

  def test_new_task_slices_one(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    now = datetime.datetime(2010, 1, 2, 3, 4, 5)
    self.mock_now(now)
    str_now = unicode(now.strftime(self.DATETIME_NO_MICRO))

    task_slices = [
      {
        u'properties': self.create_props(command=['python', 'run_test.py']),
        u'expiration_secs': 180,
        u'deny_if_no_worker': True,
      },
    ]
    response, _ = self.client_create_task(
        expiration_secs=None, task_slices=task_slices)
    expected_props = {
      u'cipd_input': {
        u'client_package': {
          u'package_name': u'infra/tools/cipd/${platform}',
          u'version': u'git_revision:deadbeef',
        },
        u'packages': [
          {
            u'package_name': u'rm',
            u'path': u'bin',
            u'version': u'git_revision:deadbeef',
          },
        ],
        u'server': u'https://chrome-infra-packages.appspot.com',
      },
      u'command': [u'python', u'run_test.py'],
      u'dimensions': [
        {u'key': u'os', u'value': u'Amiga'},
        {u'key': u'pool', u'value': u'default'},
      ],
      u'execution_timeout_secs': u'3600',
      u'grace_period_secs': u'30',
      u'idempotent': False,
      u'io_timeout_secs': u'1200',
      u'outputs': [u'foo', u'path/to/foobar'],
    }
    expected = {
      u'request': {
        u'authenticated': u'user:user@example.com',
        u'created_ts': str_now,
        u'expiration_secs': u'180',
        u'name': u'hi',
        u'priority': u'20',
        u'properties': expected_props,
        u'service_account': u'none',
        u'tags': [
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'service_account:none',
          u'user:joe@localhost',
        ],
        u'task_slices': [
          {
            u'deny_if_no_worker': True,
            u'expiration_secs': u'180',
            u'properties': expected_props,
          },
        ],
        u'user': u'joe@localhost',
      },
      u'task_id': u'5cee488008810',
    }
    self.assertEqual(expected, response)

  def test_new_task_slices_two(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    now = datetime.datetime(2010, 1, 2, 3, 4, 5)
    self.mock_now(now)
    str_now = unicode(now.strftime(self.DATETIME_NO_MICRO))

    task_slices = [
      {
        u'properties': self.create_props(command=['python', 'run_test.py']),
        u'expiration_secs': 180,
        u'deny_if_no_worker': True,
      },
      {
        u'properties': self.create_props(command=['python', 'run_test.py']),
        u'expiration_secs': 180,
        u'deny_if_no_worker': True,
      },
    ]
    response, _ = self.client_create_task(
        expiration_secs=None, task_slices=task_slices)
    expected_props = {
      u'cipd_input': {
        u'client_package': {
          u'package_name': u'infra/tools/cipd/${platform}',
          u'version': u'git_revision:deadbeef',
        },
        u'packages': [
          {
            u'package_name': u'rm',
            u'path': u'bin',
            u'version': u'git_revision:deadbeef',
          },
        ],
        u'server': u'https://chrome-infra-packages.appspot.com',
      },
      u'command': [u'python', u'run_test.py'],
      u'dimensions': [
        {u'key': u'os', u'value': u'Amiga'},
        {u'key': u'pool', u'value': u'default'},
      ],
      u'execution_timeout_secs': u'3600',
      u'grace_period_secs': u'30',
      u'idempotent': False,
      u'io_timeout_secs': u'1200',
      u'outputs': [u'foo', u'path/to/foobar'],
    }
    expected = {
      u'request': {
        u'authenticated': u'user:user@example.com',
        u'created_ts': str_now,
        # Automatically calculated: 180+180
        u'expiration_secs': u'360',
        u'name': u'hi',
        u'priority': u'20',
        u'properties': expected_props,
        u'service_account': u'none',
        u'tags': [
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'service_account:none',
          u'user:joe@localhost',
        ],
        u'task_slices': [
          {
            u'deny_if_no_worker': True,
            u'expiration_secs': u'180',
            u'properties': expected_props,
          },
          {
            u'deny_if_no_worker': True,
            u'expiration_secs': u'180',
            u'properties': expected_props,
          },
        ],
        u'user': u'joe@localhost',
      },
      u'task_id': u'5cee488008810',
    }
    self.assertEqual(expected, response)

  def test_new_task_slices_two_denied(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    now = datetime.datetime(2010, 1, 2, 3, 4, 5)
    self.mock_now(now)

    cfg = config.settings()
    cfg.isolate.default_server = 'https://isolateserver.appspot.com'
    cfg.isolate.default_namespace = 'default-gzip'
    self.mock(config, 'settings', lambda: cfg)

    task_slices = [
      {
        u'properties': self.create_props(command=['python', 'run_test.py']),
        u'expiration_secs': 180,
        u'deny_if_no_worker': True,
      },
      {
        u'properties': self.create_props(command=['python', 'run_test.py']),
        # That's incorrect:
        u'expiration_secs': 0,
        u'deny_if_no_worker': True,
      },
    ]
    request = swarming_rpcs.NewTaskRequest(
        expiration_secs=None,
        name='hi',
        priority=10,
        tags=[],
        task_slices=task_slices,
        user='joe@localhost')
    resp = self.call_api('new', body=message_to_dict(request), status=400)
    expected = {
      u'state': u'APPLICATION_ERROR',
      u'error_message': u'expiration_secs (0) must be between 1s and 7 days',
    }
    self.assertEqual(expected, resp.json)

  def test_mass_cancel(self):
    # Create two tasks.
    self.mock(random, 'getrandbits', lambda _: 0x88)
    first, second, _, _, now_120 = self._gen_three_pending_tasks()
    now_120_str = unicode(now_120.strftime(DATETIME_NO_MICRO))

    expected = {
      u'matched': u'2',
      u'now': now_120_str,
    }
    self.set_as_admin()

    def enqueue_task(*args, **kwargs):
      e = {'tasks': [second, first], 'kill_running': False}
      self.assertEqual(e, json.loads(kwargs.get('payload')))
      # check URL
      self.assertEqual('/internal/taskqueue/cancel-tasks', args[0])
      # check task queue
      self.assertEqual('cancel-tasks', args[1])
      return True
    self.mock(utils, 'enqueue_task', enqueue_task)

    response = self.call_api('cancel', body={u'tags': [u'os:Win']})
    self.assertEqual(expected, response.json)

  def test_list_ok(self):
    """Asserts that list requests all TaskResultSummaries."""
    first, second, str_now_120, start, end = self._gen_two_tasks()
    first_no_perf = first.copy()
    first_no_perf.pop('performance_stats')
    # Basic request.
    request = swarming_rpcs.TasksRequest(
        end=end, start=start, include_performance_stats=True)
    expected = {u'now': str_now_120, u'items': [second, first]}
    actual = self.call_api('list', body=message_to_dict(request)).json
    # Generate the actual expected values by decompressing the data.
    for k in ('isolated_download', 'isolated_upload'):
      for j in ('items_cold', 'items_hot'):
        actual['items'][1]['performance_stats'][k][j] = large.unpack(
            base64.b64decode(actual['items'][1]['performance_stats'][k][j]))
    self.assertEqual(expected, actual)

    # Sort by CREATED_TS.
    request = swarming_rpcs.TasksRequest(
        sort=swarming_rpcs.TaskSort.CREATED_TS)
    actual = self.call_api('list', body=message_to_dict(request)).json
    self.assertEqual(
        {u'now': str_now_120, u'items': [second, first_no_perf]}, actual)

    # Sort by MODIFIED_TS.
    request = swarming_rpcs.TasksRequest(
        sort=swarming_rpcs.TaskSort.MODIFIED_TS)
    actual = self.call_api('list', body=message_to_dict(request)).json
    self.assertEqual(
        {u'now': str_now_120, u'items': [first_no_perf, second]}, actual)

    # With two tags.
    request = swarming_rpcs.TasksRequest(
        end=end, start=start, tags=['project:yay', 'commit:pre'])
    self.assertEqual(
        {u'now': str_now_120, u'items': [second]},
        self.call_api('list', body=message_to_dict(request)).json)

    # A spurious tag.
    request = swarming_rpcs.TasksRequest(end=end, start=start, tags=['foo:bar'])
    self.assertEqual(
        {u'now': str_now_120},
        self.call_api('list', body=message_to_dict(request)).json)

    # Both state and tag.
    request = swarming_rpcs.TasksRequest(
        end=end, start=start, tags=['commit:pre'],
        state=swarming_rpcs.TaskState.COMPLETED_SUCCESS)
    self.assertEqual(
        {u'now': str_now_120, u'items': [second]},
        self.call_api('list', body=message_to_dict(request)).json)

    # Both sort and tag.
    request = swarming_rpcs.TasksRequest(
        end=end, start=start, tags=['commit:pre'],
        sort=swarming_rpcs.TaskSort.MODIFIED_TS,
        state=swarming_rpcs.TaskState.COMPLETED_SUCCESS)
    self.call_api('list', body=message_to_dict(request), status=400)

  def test_count_indexes(self):
    # Asserts that no combination crashes.
    _, _, str_now_120, start, end = self._gen_two_tasks()
    for state in swarming_rpcs.TaskState:
      for tags in ([], ['a:1'], ['a:1', 'b:2']):
        request = swarming_rpcs.TasksCountRequest(
            start=start, end=end, state=state, tags=tags)
        result = self.call_api('count', body=message_to_dict(request)).json
        # Don't check for correctness here, just assert that it doesn't throw
        # due to missing index.
        result.pop(u'count')
        expected = {u'now': str_now_120}
        self.assertEqual(expected, result)

  def test_list_indexes(self):
    # Asserts that no combination crashes unexpectedly.
    TaskState = swarming_rpcs.TaskState
    TaskSort = swarming_rpcs.TaskSort
    # List of all unsupported combinations. These can be added either with a new
    # index or by massaging the way entities are stored.
    blacklisted = [
        # (<Using start, end or tags>, TaskState, TaskSort)
        (None, TaskState.BOT_DIED, TaskSort.ABANDONED_TS),
        (None, TaskState.BOT_DIED, TaskSort.COMPLETED_TS),
        (None, TaskState.BOT_DIED, TaskSort.MODIFIED_TS),
        (None, TaskState.CANCELED, TaskSort.ABANDONED_TS),
        (None, TaskState.CANCELED, TaskSort.COMPLETED_TS),
        (None, TaskState.CANCELED, TaskSort.MODIFIED_TS),
        (None, TaskState.COMPLETED, TaskSort.ABANDONED_TS),
        (None, TaskState.COMPLETED, TaskSort.COMPLETED_TS),
        (None, TaskState.COMPLETED, TaskSort.MODIFIED_TS),
        (None, TaskState.COMPLETED_FAILURE, TaskSort.ABANDONED_TS),
        (None, TaskState.COMPLETED_FAILURE, TaskSort.COMPLETED_TS),
        (None, TaskState.COMPLETED_FAILURE, TaskSort.MODIFIED_TS),
        (None, TaskState.COMPLETED_SUCCESS, TaskSort.ABANDONED_TS),
        (None, TaskState.COMPLETED_SUCCESS, TaskSort.COMPLETED_TS),
        (None, TaskState.COMPLETED_SUCCESS, TaskSort.MODIFIED_TS),
        (None, TaskState.DEDUPED, TaskSort.ABANDONED_TS),
        (None, TaskState.DEDUPED, TaskSort.COMPLETED_TS),
        (None, TaskState.DEDUPED, TaskSort.MODIFIED_TS),
        (None, TaskState.EXPIRED, TaskSort.ABANDONED_TS),
        (None, TaskState.EXPIRED, TaskSort.COMPLETED_TS),
        (None, TaskState.EXPIRED, TaskSort.MODIFIED_TS),
        (None, TaskState.KILLED, TaskSort.ABANDONED_TS),
        (None, TaskState.KILLED, TaskSort.COMPLETED_TS),
        (None, TaskState.KILLED, TaskSort.MODIFIED_TS),
        (None, TaskState.PENDING, TaskSort.ABANDONED_TS),
        (None, TaskState.PENDING, TaskSort.COMPLETED_TS),
        (None, TaskState.PENDING, TaskSort.MODIFIED_TS),
        (None, TaskState.PENDING_RUNNING, TaskSort.ABANDONED_TS),
        (None, TaskState.PENDING_RUNNING, TaskSort.COMPLETED_TS),
        (None, TaskState.PENDING_RUNNING, TaskSort.MODIFIED_TS),
        (None, TaskState.RUNNING, TaskSort.ABANDONED_TS),
        (None, TaskState.RUNNING, TaskSort.COMPLETED_TS),
        (None, TaskState.RUNNING, TaskSort.MODIFIED_TS),
        (None, TaskState.TIMED_OUT, TaskSort.ABANDONED_TS),
        (None, TaskState.TIMED_OUT, TaskSort.COMPLETED_TS),
        (None, TaskState.TIMED_OUT, TaskSort.MODIFIED_TS),
        (True, TaskState.ALL, TaskSort.ABANDONED_TS),
        (True, TaskState.ALL, TaskSort.COMPLETED_TS),
        (True, TaskState.ALL, TaskSort.MODIFIED_TS),
    ]
    _, _, str_now_120, start, end = self._gen_two_tasks()
    for state in TaskState:
      for tags in ([], ['a:1'], ['a:1', 'b:2']):
        for start in (None, start):
          for end in (None, end):
            for sort in TaskSort:
              request = swarming_rpcs.TasksRequest(
                  start=start, end=end, state=state, tags=tags, sort=sort)
              using_filter = bool(start or end or tags)
              if ((using_filter, state, sort) in blacklisted or
                  (None, state, sort) in blacklisted):
                try:
                  self.call_api(
                      'list', body=message_to_dict(request), status=400)
                except:  # pylint: disable=bare-except
                  self.fail(
                      'Is actually supported: (%s, %s, %s)' %
                      (using_filter, state, sort))
              else:
                try:
                  result = self.call_api(
                      'list', body=message_to_dict(request)).json
                except:  # pylint: disable=bare-except
                  self.fail(
                      'Is unsupported: (%s, %s, %s)' %
                      (using_filter, state, sort))
                # Don't check for correctness here, just assert that it doesn't
                # throw due to missing index or invalid query.
                result.pop(u'items', None)
                expected = {u'now': str_now_120}
                self.assertEqual(expected, result)

  def test_tags_ok(self):
    """Asserts that TasksTags is returned with the right data."""
    self.set_as_privileged_user()
    task_result.TagAggregation(
        key=task_result.TagAggregation.KEY,
        tags=[
            task_result.TagValues(
                tag='foo', values=['alpha', 'beta']),
            task_result.TagValues(
                tag='bar', values=['gamma', 'delta', 'epsilon']),
        ],
        ts=self.now).put()
    expected = {
      u'tasks_tags': [
        {
          u'key': u'foo',
          u'value': [u'alpha', u'beta'],
        },
        {
          u'key': u'bar',
          u'value': [u'gamma', u'delta', u'epsilon'],
        },
      ],
      u'ts': unicode(self.now.strftime(DATETIME_NO_MICRO)),
    }
    self.assertEqual(expected, self.call_api('tags', body={}).json)

  def _gen_two_tasks(self):
    # first request
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    _, first_id = self.client_create_task_raw(
        name='first',
        tags=['project:yay', 'commit:post'],
        properties=dict(idempotent=True))
    self.set_as_bot()
    self.bot_run_task()

    # second request
    self.set_as_user()
    self.mock(random, 'getrandbits', lambda _: 0x66)
    now_60 = self.mock_now(self.now, 60)
    str_now_60 = unicode(now_60.strftime(DATETIME_NO_MICRO))
    self.client_create_task_raw(
        name='second',
        user='jack@localhost',
        tags=['project:yay', 'commit:pre'],
        properties=dict(idempotent=True))

    # Hack the datastore so MODIFIED_TS returns in backward order compared to
    # CREATED_TS.
    now_120 = self.mock_now(self.now, 120)
    str_now_120 = unicode(now_120.strftime(DATETIME_NO_MICRO))
    entity = task_pack.unpack_result_summary_key(first_id).get()
    entity.modified_ts = now_120
    entity.put()

    first = self.gen_result_summary(
        completed_ts=str_now,
        costs_usd=[0.1],
        created_ts=str_now,
        duration=0.1,
        exit_code=u'0',
        modified_ts=str_now_120,
        name=u'first',
        performance_stats=self.gen_perf_stats(),
        started_ts=str_now,
        tags=[
          u'commit:post', u'os:Amiga', u'pool:default', u'priority:20',
          u'project:yay', u'service_account:none', u'user:joe@localhost',
        ],
        try_number=u'1')
    deduped = self.gen_result_summary(
        completed_ts=str_now,
        cost_saved_usd=0.1,
        created_ts=str_now_60,
        deduped_from=u'5cee488008811',
        duration=0.1,
        exit_code=u'0',
        modified_ts=str_now_60,
        name=u'second',
        run_id=u'5cee488008811',
        started_ts=str_now,
        tags=[
          u'commit:pre', u'os:Amiga', u'pool:default', u'priority:20',
          u'project:yay', u'service_account:none', u'user:jack@localhost',
        ],
        task_id=u'5cfcee8006610',
        user=u'jack@localhost')

    start = (
        utils.datetime_to_timestamp(self.now - datetime.timedelta(days=1)) /
        1000000.)
    end = (
        utils.datetime_to_timestamp(self.now + datetime.timedelta(days=1)) /
        1000000.)
    self.set_as_privileged_user()
    return first, deduped, str_now_120, start, end

  def _gen_three_pending_tasks(self):
    # Creates three pending tasks, spaced 1 minute apart
    self.mock(random, 'getrandbits', lambda _: 0x66)
    _, first_id = self.client_create_task_raw(
        name='first', tags=['project:yay', 'commit:abcd', 'os:Win'],
        pubsub_topic='projects/abc/topics/def',
        pubsub_userdata='1234',
        properties=dict(idempotent=True))

    now_60 = self.mock_now(self.now, 60)
    self.mock(random, 'getrandbits', lambda _: 0x88)
    _, second_id = self.client_create_task_raw(
        name='second', user='jack@localhost',
        pubsub_topic='projects/abc/topics/def',
        pubsub_userdata='5678',
        tags=['project:yay', 'commit:efgh', 'os:Win'],
        properties=dict(idempotent=True))

    now_120 = self.mock_now(self.now, 120)
    _, third_id = self.client_create_task_raw(
        name='third', user='jack@localhost',
        pubsub_topic='projects/abc/topics/def',
        pubsub_userdata='9000',
        tags=['project:yay', 'commit:ijkhl', 'os:Linux'],
        properties=dict(idempotent=True))

    return first_id, second_id, third_id, now_60, now_120


class TaskApiTest(BaseTest):
  api_service_cls = handlers_endpoints.SwarmingTaskService

  def setUp(self):
    super(TaskApiTest, self).setUp()
    self.tasks_api = test_case.Endpoints(
        handlers_endpoints.SwarmingTasksService)

  def test_cancel_pending(self):
    """Asserts that task cancellation goes smoothly."""
    # catch PubSub notification
    # Create and cancel a task as a non-privileged user.
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    _, task_id = self.client_create_task_raw(
        pubsub_topic='projects/abc/topics/def',
        pubsub_userdata='blah')
    expected = {u'ok': True, u'was_running': False}
    response = self.call_api(
        'cancel', body={'task_id': task_id, 'kill_running': False})
    self.assertEqual(expected, response.json)

    # determine that the task's state updates correctly
    expected = {
      u'abandoned_ts': str_now,
      u'created_ts': str_now,
      u'failure': False,
      u'internal_failure': False,
      u'modified_ts': str_now,
      u'name': u'job1',
      u'server_versions': [u'v1a'],
      u'state': u'CANCELED',
      u'tags': [
        u'a:tag',
        u'os:Amiga',
        u'pool:default',
        u'priority:20',
        u'service_account:none',
        u'user:joe@localhost',
      ],
      u'task_id': task_id,
      u'task_slice_index': u'0',
      u'user': u'joe@localhost',
    }
    response = self.call_api('result', body={'task_id': task_id})
    self.assertEqual(expected, response.json)

    # notification has been sent.
    expected = [
      {
        'payload': '{"auth_token":null,"task_id":"5cee488008810",'
                   '"topic":"projects/abc/topics/def","userdata":"blah"}',
        'queue_name': 'pubsub',
        'transactional': True,
        'url': '/internal/taskqueue/pubsub/5cee488008810',
      },
    ]

  def test_cancel_forbidden(self):
    """Asserts that non-privileged non-owner can't cancel tasks."""
    # Create a task as an admin.
    self.mock(random, 'getrandbits', lambda _: 0x88)
    self.set_as_admin()
    _, task_id = self.client_create_task_raw(
        pubsub_topic='projects/abc/topics/def',
        pubsub_userdata='blah')

    # Attempt to cancel as non-privileged user -> HTTP 403.
    self.set_as_user()
    self.call_api(
        'cancel', body={'task_id': task_id, 'kill_running': False}, status=403)

  def test_cancel_running(self):
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    _, task_id = self.client_create_task_raw(
        properties=dict(command=['python', 'runtest.py']))

    self.set_as_bot()
    params = self.do_handshake()
    data = self.post_json('/swarming/api/v1/bot/poll', params)
    run_id = data['manifest']['task_id']
    def _params(**kwargs):
      out = {
        'cost_usd': 0.1,
        'duration': None,
        'exit_code': None,
        'id': 'bot1',
        'output': None,
        'output_chunk_start': 0,
        'task_id': run_id,
      }
      out.update(**kwargs)
      return out

    self.set_as_bot()
    params = _params(output=base64.b64encode('Oh '))
    response = self.post_json('/swarming/api/v1/bot/task_update', params)
    self.assertEqual({u'must_stop': False, u'ok': True}, response)
    self.set_as_user()
    expected = self.gen_result_summary(
        costs_usd=[0.1],
        created_ts=str_now,
        modified_ts=str_now,
        started_ts=str_now,
        state=u'RUNNING',
        try_number=u'1')
    self.assertEqual(expected, self.client_get_results(task_id))

    # Denied if kill_running == False.
    response = self.call_api(
        'cancel', body={'task_id': task_id, 'kill_running': False})
    self.assertEqual({u'ok': False, u'was_running': True}, response.json)

    # Works if kill_running == True.
    response = self.call_api(
        'cancel', body={'task_id': task_id, 'kill_running': True})
    self.assertEqual({u'ok': True, u'was_running': True}, response.json)

    self.set_as_bot()
    params = _params(output=base64.b64encode('hi'), output_chunk_start=3)
    response = self.post_json('/swarming/api/v1/bot/task_update', params)
    self.assertEqual({u'must_stop': True, u'ok': True}, response)

    # abandoned_ts is set but state isn't changed yet.
    self.set_as_user()
    expected = self.gen_result_summary(
        abandoned_ts=str_now,
        costs_usd=[0.1],
        created_ts=str_now,
        modified_ts=str_now,
        started_ts=str_now,
        state=u'RUNNING',
        try_number=u'1')
    self.assertEqual(expected, self.client_get_results(task_id))

    # Bot terminates the task.
    self.set_as_bot()
    params = _params(
        output=base64.b64encode(' again'), output_chunk_start=6,
        duration=0.1, exit_code=0)
    response = self.post_json('/swarming/api/v1/bot/task_update', params)
    self.assertEqual({u'must_stop': True, u'ok': True}, response)

    self.set_as_user()
    expected = self.gen_result_summary(
        abandoned_ts=str_now,
        costs_usd=[0.1],
        created_ts=str_now,
        duration=0.1,
        exit_code=u'0',
        modified_ts=str_now,
        started_ts=str_now,
        state=u'KILLED',
        try_number=u'1')
    self.assertEqual(expected, self.client_get_results(task_id))

  def test_result_unknown(self):
    """Asserts that result raises 404 for unknown task IDs."""
    self.call_api('result', body={'task_id': '12310'}, status=404)

  def test_result_ok(self):
    """Asserts that result produces a result entity."""
    self.mock(random, 'getrandbits', lambda _: 0x88)

    # pending task
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    _, task_id = self.client_create_task_raw()
    response = self.call_api('result', body={'task_id': task_id})
    expected = {
      u'created_ts': str_now,
      u'failure': False,
      u'internal_failure': False,
      u'modified_ts': str_now,
      u'name': u'job1',
      u'server_versions': [u'v1a'],
      u'state': u'PENDING',
      u'tags': [
        u'a:tag',
        u'os:Amiga',
        u'pool:default',
        u'priority:20',
        u'service_account:none',
        u'user:joe@localhost',
      ],
      u'task_id': u'5cee488008810',
      u'task_slice_index': u'0',
      u'user': u'joe@localhost',
    }
    self.assertEqual(expected, response.json)

    # no bot started: running task
    run_id = task_id[:-1] + '1'
    self.call_api('result', body={'task_id': run_id}, status=404)

    # run as bot
    self.set_as_bot()
    self.bot_poll('bot1')

    self.set_as_user()
    response = self.call_api('result', body={'task_id': run_id})
    expected = self.gen_run_result(
        created_ts=str_now,
        modified_ts=str_now,
        started_ts=str_now)
    self.assertEqual(expected, response.json)

  def test_result_completed_task(self):
    """Tests that completed tasks are correctly reported."""
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    self.client_create_task_raw()
    self.set_as_bot()
    task_id = self.bot_run_task()
    # First ask without perf metadata.
    self.set_as_user()
    response = self.call_api('result', body={'task_id': task_id})
    expected = self.gen_run_result(
        completed_ts=str_now,
        costs_usd=[0.1],
        created_ts=str_now,
        duration=0.1,
        exit_code=u'0',
        modified_ts=str_now,
        run_id=task_id,
        started_ts=str_now,
        state=u'COMPLETED',
        task_id=task_id)
    self.assertEqual(expected, response.json)

    expected[u'performance_stats'] = self.gen_perf_stats()
    response = self.call_api(
        'result',
        body={'task_id': task_id, 'include_performance_stats': True})
    actual = response.json
    for k in ('isolated_download', 'isolated_upload'):
      for j in ('items_cold', 'items_hot'):
        actual['performance_stats'][k][j] = large.unpack(
            base64.b64decode(actual['performance_stats'][k][j]))
    self.assertEqual(expected, actual)

  def test_stdout_ok(self):
    """Asserts that stdout reports a task's output."""
    self.client_create_task_raw()

    # task_id determined by bot run
    self.set_as_bot()
    task_id = self.bot_run_task()

    self.set_as_privileged_user()
    run_id = task_id[:-1] + '1'
    expected = {u'output': u'rÉsult string'}
    for i in (task_id, run_id):
      response = self.call_api('stdout', body={'task_id': i})
      self.assertEqual(expected, response.json)

  def test_stdout_empty(self):
    """Asserts that incipient tasks produce no output."""
    _, task_id = self.client_create_task_raw()
    response = self.call_api('stdout', body={'task_id': task_id})
    self.assertEqual({}, response.json)

    run_id = task_id[:-1] + '1'
    self.call_api('stdout', body={'task_id': run_id}, status=404)

  def test_result_run_not_found(self):
    """Asserts that getting results from incipient tasks raises 404."""
    _, task_id = self.client_create_task_raw()
    run_id = task_id[:-1] + '1'
    self.call_api('stdout', body={'task_id': run_id}, status=404)

  def test_task_deduped(self):
    """Asserts that task deduplication works as expected."""
    _, task_id_1 = self.client_create_task_raw(properties=dict(idempotent=True))

    self.set_as_bot()
    task_id_bot = self.bot_run_task()
    self.assertEqual(task_id_1, task_id_bot[:-1] + '0')
    self.assertEqual('1', task_id_bot[-1:])

    # second task; this one's results should be returned immediately
    self.set_as_user()
    _, task_id_2 = self.client_create_task_raw(
        name='second', user='jack@localhost', properties=dict(idempotent=True))

    self.set_as_bot()
    resp = self.bot_poll()
    self.assertEqual('sleep', resp['cmd'])

    self.set_as_user()

    # results shouldn't change, even if the second task wasn't executed
    response = self.call_api('stdout', body={'task_id': task_id_2})
    self.assertEqual({'output': u'rÉsult string'}, response.json)

  def test_request_unknown(self):
    """Asserts that 404 is raised for unknown tasks."""
    self.call_api('request', body={'task_id': '12310'}, status=404)

  def test_request_ok(self):
    """Asserts that request produces a task request."""
    self.mock_task_service_accounts()
    self.mock_default_pool_acl(['service-account@example.com'])
    _, task_id = self.client_create_task_raw(
        properties={'secret_bytes': 'zekret'},
        service_account='service-account@example.com')

    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))
    expected = self.gen_request(
        created_ts=str_now,
        properties=self.gen_props(
            command=[u'python', u'run_test.py'],
            secret_bytes=u'PFJFREFDVEVEPg=='), # <REDACTED> in base64
        service_account=u'service-account@example.com',
        tags=[
          u'a:tag',
          u'os:Amiga',
          u'pool:default',
          u'priority:20',
          u'service_account:service-account@example.com',
          u'user:joe@localhost',
        ])
    response = self.call_api('request', body={'task_id': task_id})
    self.assertEqual(expected, response.json)


class BotsApiTest(BaseTest):
  api_service_cls = handlers_endpoints.SwarmingBotsService

  def test_list_ok(self):
    """Asserts that BotInfo is returned for the appropriate set of bots."""
    self.set_as_privileged_user()
    then = datetime.datetime(2009, 1, 2, 3, 4, 5)
    then_str = unicode(then.strftime(DATETIME_NO_MICRO))
    self.mock_now(then)

    # Add three bot events, corresponding to one dead bot, one quarantined bot,
    # and one good bot
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id3',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id3'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=False, task_id=None, task_name=None,
        machine_type='mt')
    self.mock_now(self.now)
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id1',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id1'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=False, task_id=None, task_name=None)
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id2',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id2'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=True, task_id=None, task_name=None)
    now_str = unicode(self.now.strftime(DATETIME_NO_MICRO))
    bot1 = {
      u'authenticated_as': u'bot:whitelisted-ip',
      u'bot_id': u'id1',
      u'deleted': False,
      u'dimensions': [
        {u'key': u'id', u'value': [u'id1']},
        {u'key': u'pool', u'value': [u'default']},
      ],
      u'external_ip': u'8.8.4.4',
      u'first_seen_ts': now_str,
      u'is_dead': False,
      u'last_seen_ts': now_str,
      u'quarantined': False,
      u'state': u'{"ram":65}',
      u'version': u'123456789',
    }
    bot2 = {
      u'authenticated_as': u'bot:whitelisted-ip',
      u'bot_id': u'id2',
      u'deleted': False,
      u'dimensions': [
        {u'key': u'id', u'value': [u'id2']},
        {u'key': u'pool', u'value': [u'default']},
      ],
      u'external_ip': u'8.8.4.4',
      u'first_seen_ts': now_str,
      u'is_dead': False,
      u'last_seen_ts': now_str,
      u'quarantined': True,
      u'state': u'{"ram":65}',
      u'version': u'123456789',
    }
    bot3 = {
      u'authenticated_as': u'bot:whitelisted-ip',
      u'bot_id': u'id3',
      u'deleted': False,
      u'dimensions': [
        {u'key': u'id', u'value': [u'id3']},
        {u'key': u'pool', u'value': [u'default']},
      ],
      u'external_ip': u'8.8.4.4',
      u'first_seen_ts': then_str,
      u'is_dead': True,
      u'last_seen_ts': then_str,
      u'machine_type': u'mt',
      u'quarantined': False,
      u'state': u'{"ram":65}',
      u'version': u'123456789',
    }
    expected = {
      u'items': [bot1, bot2, bot3],
      u'death_timeout': unicode(config.settings().bot_death_timeout_secs),
      u'now': now_str,
    }
    # All bots should be returned with no params
    request = swarming_rpcs.BotsRequest()
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # All bots should be returned if we don't care about quarantined
    request = swarming_rpcs.BotsRequest(
        quarantined=swarming_rpcs.ThreeStateBool.NONE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # All bots should be returned if we don't care about is_dead
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.NONE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # Only bot1 corresponds to these two dimensions
    expected[u'items'] = [bot1]
    request = swarming_rpcs.BotsRequest(dimensions=['pool:default', 'id:id1'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # Only bot1 corresponds to being not dead and not quarantined and
    # this dimension
    request = swarming_rpcs.BotsRequest(
      dimensions=['pool:default'],
      quarantined=swarming_rpcs.ThreeStateBool.FALSE,
      is_dead=swarming_rpcs.ThreeStateBool.FALSE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # exclude bot2 only, which is quarantined
    expected[u'items'] = [bot1, bot3]
    request = swarming_rpcs.BotsRequest(
        quarantined=swarming_rpcs.ThreeStateBool.FALSE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # exclude bot3 only, which is dead
    expected[u'items'] = [bot1, bot2]
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.FALSE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # only bot2 is quarantined
    expected[u'items'] = [bot2]
    request = swarming_rpcs.BotsRequest(
        quarantined=swarming_rpcs.ThreeStateBool.TRUE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # quarantined:true can be paired with other dimensions and still work
    request = swarming_rpcs.BotsRequest(
        quarantined=swarming_rpcs.ThreeStateBool.TRUE,
        dimensions=['pool:default'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # only bot3 is dead
    expected[u'items'] = [bot3]
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.TRUE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # is_dead:true can be paired with other dimensions and still work
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.TRUE, dimensions=['pool:default'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # only 1 bot is "ready for work"
    expected[u'items'] = [bot1]
    request = swarming_rpcs.BotsRequest(
        is_busy=swarming_rpcs.ThreeStateBool.FALSE,
        is_dead=swarming_rpcs.ThreeStateBool.FALSE,
        quarantined=swarming_rpcs.ThreeStateBool.FALSE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # only bot3 is a machine provider bot
    expected[u'items'] = [bot3]
    request = swarming_rpcs.BotsRequest(is_mp=swarming_rpcs.ThreeStateBool.TRUE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    expected[u'items'] = [bot1, bot2]
    request = swarming_rpcs.BotsRequest(
        is_mp=swarming_rpcs.ThreeStateBool.FALSE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # not:existing is a dimension that doesn't exist, nothing returned.
    request = swarming_rpcs.BotsRequest(dimensions=['not:existing'])
    response = self.call_api('list', body=message_to_dict(request))
    del expected[u'items']
    self.assertEqual(expected, response.json)
    # quarantined:true can be paired with other non-existing dimensions and
    # still work
    request = swarming_rpcs.BotsRequest(
        quarantined=swarming_rpcs.ThreeStateBool.TRUE, dimensions=['not:exist'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # is_dead:true can be paired with other non-existing dimensions and
    # still work
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.TRUE, dimensions=['not:exist'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # is_mp:true can be paired with other non-existing dimensions and still work
    request = swarming_rpcs.BotsRequest(
        is_mp=swarming_rpcs.ThreeStateBool.TRUE, dimensions=['not:exist'])
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # No bot is both dead and quarantined
    request = swarming_rpcs.BotsRequest(
        is_dead=swarming_rpcs.ThreeStateBool.TRUE,
        quarantined=swarming_rpcs.ThreeStateBool.TRUE)
    response = self.call_api('list', body=message_to_dict(request))
    self.assertEqual(expected, response.json)
    # A bad request returns 400
    request = swarming_rpcs.BotsRequest(dimensions=['bad'])
    self.call_api('list', body=message_to_dict(request), status=400)

  def test_count_ok(self):
    """Asserts that BotsCount is returned for the appropriate set of bots."""
    self.set_as_privileged_user()
    then = datetime.datetime(2009, 1, 2, 3, 4, 5)
    self.mock_now(then)
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id3',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id3'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=True, task_id=None, task_name=None)
    self.mock_now(self.now)
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id1',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id1'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=False, task_id='987', task_name=None)
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id2',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id2'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=True, task_id=None, task_name=None)
    expected = {
      u'count': u'3',
      u'quarantined': u'2',
      u'dead': u'1',
      u'busy': u'1',
      u'now': unicode(self.now.strftime(DATETIME_NO_MICRO)),
    }
    request = swarming_rpcs.BotsRequest()
    response = self.call_api('count', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

    expected = {
      u'count': u'1',
      u'quarantined': u'0',
      u'dead': u'0',
      u'busy': u'1',
      u'now': unicode(self.now.strftime(DATETIME_NO_MICRO)),
    }
    request = swarming_rpcs.BotsCountRequest(
        dimensions=['pool:default', 'id:id1'])
    response = self.call_api('count', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

    expected[u'quarantined'] = u'1'
    expected[u'busy'] = u'0'
    request = swarming_rpcs.BotsCountRequest(
        dimensions=['pool:default', 'id:id2'])
    response = self.call_api('count', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

    expected[u'dead'] = u'1'
    request = swarming_rpcs.BotsCountRequest(
        dimensions=['pool:default', 'id:id3'])
    response = self.call_api('count', body=message_to_dict(request))
    self.assertEqual(expected, response.json)

    request = swarming_rpcs.BotsCountRequest(dimensions=['not:existing'])
    response = self.call_api('count', body=message_to_dict(request))
    expected = {
      u'count': u'0',
      u'quarantined': u'0',
      u'dead': u'0',
      u'busy': u'0',
      u'now': unicode(self.now.strftime(DATETIME_NO_MICRO)),
    }
    self.assertEqual(expected, response.json)

    request = swarming_rpcs.BotsCountRequest(dimensions=['bad'])
    self.call_api('count', body=message_to_dict(request), status=400)

  def test_dimensions_ok(self):
    """Asserts that BotsDimensions is returned with the right data."""
    self.set_as_privileged_user()

    bot_management.DimensionAggregation(
        key=bot_management.DimensionAggregation.KEY,
        dimensions=[
            bot_management.DimensionValues(
              dimension='foo', values=['alpha', 'beta']),
            bot_management.DimensionValues(
              dimension='bar', values=['gamma', 'delta', 'epsilon']),
        ],
        ts=self.now).put()

    expected = {
      u'bots_dimensions': [
        {
          u'key': u'foo',
          u'value': [u'alpha', u'beta'],
        },
        {
          u'key': u'bar',
          u'value': [u'gamma', u'delta', u'epsilon'],
        },
      ],
      u'ts': unicode(self.now.strftime(DATETIME_NO_MICRO)),
    }

    self.assertEqual(expected, self.call_api('dimensions', body={}).json)


class BotApiTest(BaseTest):
  api_service_cls = handlers_endpoints.SwarmingBotService

  def test_get_ok(self):
    """Asserts that get shows the tasks a specific bot has executed."""
    self.set_as_privileged_user()
    now_str = unicode(self.now.strftime(DATETIME_NO_MICRO))
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id1',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id1'], u'pool': [u'default']}, state={'ram': 65},
        version='123456789', quarantined=False, task_id=None, task_name=None)

    expected = {
      u'authenticated_as': u'bot:whitelisted-ip',
      u'bot_id': u'id1',
      u'deleted': False,
      u'dimensions': [
        {u'key': u'id', u'value': [u'id1']},
        {u'key': u'pool', u'value': [u'default']},
      ],
      u'external_ip': u'8.8.4.4',
      u'first_seen_ts': now_str,
      u'is_dead': False,
      u'last_seen_ts': now_str,
      u'quarantined': False,
      u'state': u'{"ram":65}',
      u'version': u'123456789',
    }
    response = self.call_api('get', body={'bot_id': 'id1'})
    self.assertEqual(expected, response.json)

  def test_get_no_bot(self):
    """Asserts that get raises 404 when no bot is found."""
    self.set_as_admin()
    self.call_api('get', body={'bot_id': 'not_a_bot'}, status=404)

  def test_delete_ok(self):
    """Assert that delete finds and deletes a bot."""
    self.set_as_admin()
    self.mock(acl, '_is_admin', lambda *_args, **_kwargs: True)
    state = {
      'dict': {'random': 'values'},
      'float': 0.,
      'list': ['of', 'things'],
      'str': u'uni',
    }
    bot_management.bot_event(
        event_type='bot_connected', bot_id='id1',
        external_ip='8.8.4.4', authenticated_as='bot:whitelisted-ip',
        dimensions={u'id': [u'id1'], u'pool': [u'default']}, state=state,
        version='123456789', quarantined=False, task_id=None, task_name=None)

    # delete the bot
    response = self.call_api('delete', body={'bot_id': 'id1'})
    self.assertEqual({u'deleted': True}, response.json)

    # is it gone?
    self.call_api('delete', body={'bot_id': 'id1'}, status=404)

  def test_tasks_ok(self):
    """Asserts that tasks produces bot information."""
    self.mock(random, 'getrandbits', lambda _: 0x88)

    self.set_as_bot()
    self.client_create_task_raw()
    res = self.bot_poll()
    response = self.bot_complete_task(task_id=res['manifest']['task_id'])
    self.assertEqual({u'must_stop': False, u'ok': True}, response)

    now_1 = self.mock_now(self.now, 1)
    now_1_str = unicode(now_1.strftime(DATETIME_NO_MICRO))
    self.mock(random, 'getrandbits', lambda _: 0x55)
    self.client_create_task_raw(name='philbert')
    res = self.bot_poll()
    response = self.bot_complete_task(
        exit_code=1, task_id=res['manifest']['task_id'])
    self.assertEqual({u'must_stop': False, u'ok': True}, response)

    start = utils.datetime_to_timestamp(
        self.now + datetime.timedelta(seconds=0.5)) / 1000000.
    end = utils.datetime_to_timestamp(
        now_1 + datetime.timedelta(seconds=0.5)) / 1000000.

    self.set_as_privileged_user()
    request = swarming_rpcs.BotTasksRequest(
        end=end, start=start, include_performance_stats=True)
    body = message_to_dict(request)
    body['bot_id'] = 'bot1'
    response = self.call_api('tasks', body=body)
    expected = {
      u'items': [
        self.gen_run_result(
            completed_ts=now_1_str,
            costs_usd=[0.1],
            created_ts=now_1_str,
            duration=0.1,
            exit_code=u'1',
            failure=True,
            modified_ts=now_1_str,
            name=u'philbert',
            performance_stats=self.gen_perf_stats(),
            run_id=u'5cee870005511',
            started_ts=now_1_str,
            state=u'COMPLETED',
            task_id=u'5cee870005511'),
      ],
      u'now': now_1_str,
    }
    actual = response.json
    for k in ('isolated_download', 'isolated_upload'):
      for j in ('items_cold', 'items_hot'):
        actual['items'][0]['performance_stats'][k][j] = large.unpack(
            base64.b64decode(actual['items'][0]['performance_stats'][k][j]))
    self.assertEqual(expected, actual)

  def test_events(self):
    # Run one task, push an event manually.
    self.mock(random, 'getrandbits', lambda _: 0x88)
    str_now = unicode(self.now.strftime(DATETIME_NO_MICRO))

    self.set_as_bot()
    self.client_create_task_raw()
    params = self.do_handshake()
    res = self.bot_poll()
    now_60 = self.mock_now(self.now, 60)
    str_now_60 = unicode(now_60.strftime(DATETIME_NO_MICRO))
    response = self.bot_complete_task(task_id=res['manifest']['task_id'])
    self.assertEqual({u'must_stop': False, u'ok': True}, response)

    params['event'] = 'bot_rebooting'
    params['message'] = 'for the best'
    response = self.post_json('/swarming/api/v1/bot/event', params)
    self.assertEqual({}, response)

    start = utils.datetime_to_timestamp(self.now) / 1000000.
    end = utils.datetime_to_timestamp(now_60) / 1000000.
    self.set_as_privileged_user()
    body = message_to_dict(
        swarming_rpcs.BotEventsRequest(start=start, end=end+1))
    body['bot_id'] = 'bot1'
    response = self.call_api('events', body=body)
    dimensions = [
      {u'key': u'id', u'value': [u'bot1']},
      {u'key': u'os', u'value': [u'Amiga']},
      {u'key': u'pool', u'value': [u'default']},
    ]
    state_dict = {
      'bot_group_cfg_version': 'default',
      'running_time': 1234.,
      'sleep_streak': 0,
      'started_ts': 1410990411.111,
    }
    state = unicode(
        json.dumps(state_dict, sort_keys=True, separators=(',', ':')))
    state_dict.pop('bot_group_cfg_version')
    state_no_cfg_ver = unicode(
        json.dumps(state_dict, sort_keys=True, separators=(',', ':')))
    expected = {
      u'items': [
        {
          u'authenticated_as': u'bot:whitelisted-ip',
          u'dimensions': dimensions,
          u'event_type': u'bot_rebooting',
          u'external_ip': unicode(self.source_ip),
          u'message': u'for the best',
          u'quarantined': False,
          u'state': state,
          u'ts': str_now_60,
          u'version': unicode(self.bot_version),
        },
        {
          u'authenticated_as': u'bot:whitelisted-ip',
          u'dimensions': dimensions,
          u'event_type': u'task_completed',
          u'external_ip': unicode(self.source_ip),
          u'quarantined': False,
          u'state': state,
          u'task_id': u'5cee488008811',
          u'ts': str_now_60,
          u'version': unicode(self.bot_version),
        },
        {
          u'authenticated_as': u'bot:whitelisted-ip',
          u'dimensions': dimensions,
          u'event_type': u'request_task',
          u'external_ip': unicode(self.source_ip),
          u'quarantined': False,
          u'state': state,
          u'task_id': u'5cee488008811',
          u'ts': str_now,
          u'version': unicode(self.bot_version),
        },
        {
          u'authenticated_as': u'bot:whitelisted-ip',
          u'dimensions': dimensions,
          u'event_type': u'bot_connected',
          u'external_ip': unicode(self.source_ip),
          u'quarantined': False,
          u'state': state_no_cfg_ver,
          u'ts': str_now,
          u'version': u'123',
        },
        {
          u'authenticated_as': u'bot:whitelisted-ip',
          u'dimensions': dimensions,
          u'event_type': u'bot_connected',
          u'external_ip': unicode(self.source_ip),
          u'quarantined': False,
          u'state': state_no_cfg_ver,
          u'ts': str_now,
          u'version': u'123',
        },
      ],
        u'now': str_now_60,
    }
    self.assertEqual(expected, response.json)

    # Now test with a subset.
    body = message_to_dict(swarming_rpcs.BotEventsRequest(start=end, end=end+1))
    body['bot_id'] = 'bot1'
    response = self.call_api('events', body=body)
    expected['items'] = expected['items'][:-3]
    self.assertEqual(expected, response.json)

  def test_terminate_admin(self):
    self.set_as_bot()
    self.bot_poll()
    self.mock(random, 'getrandbits', lambda _: 0x88)

    self.set_as_admin()
    response = self.call_api('terminate', body={'bot_id': 'bot1'})
    self.assertEqual({u'task_id': u'5cee488008810'}, response.json)

  def test_terminate_privileged_user(self):
    self.set_as_bot()
    self.bot_poll()
    self.mock(random, 'getrandbits', lambda _: 0x88)

    self.set_as_privileged_user()
    response = self.call_api('terminate', body={'bot_id': 'bot1'})
    self.assertEqual({u'task_id': u'5cee488008810'}, response.json)

  def test_terminate_user(self):
    self.set_as_bot()
    self.bot_poll()

    self.set_as_user()
    self.call_api('terminate', body={'bot_id': 'bot1'}, status=403)


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.CRITICAL)
  unittest.main()
