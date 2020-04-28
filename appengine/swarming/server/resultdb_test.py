#!/usr/bin/env vpython
# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import logging
import sys
import unittest
import uuid

import mock

import test_env
test_env.setup_test_env()

from google.appengine.api import app_identity

from test_support import test_case

from components import net

from server import config
from server import resultdb

from proto.config import config_pb2


class ResultDBTest(test_case.TestCase):
  # This test needs to be run independently
  # run by test.py
  no_run = 1

  def setUp(self):
    super(ResultDBTest, self).setUp()
    mock.patch('google.appengine.api.app_identity.get_default_version_hostname'
              ).start().return_value = 'test-swarming.appspot.com'
    mock.patch('uuid.uuid4').start().return_value = uuid.UUID(int=0)

  def tearDown(self):
    super(ResultDBTest, self).tearDown()
    mock.patch.stopall()

  def test_create_invocation(self):

    def mock_call_resultdb_recorder_api(_method, _request, response_headers):
      response_headers['update-token'] = 'token'

    with mock.patch(
        'server.resultdb._call_resultdb_recorder_api',
        mock.MagicMock(
            side_effect=mock_call_resultdb_recorder_api)) as mock_call:

      update_token = resultdb.create_invocation('task001')
      self.assertEqual(update_token, 'token')
      mock_call.assert_called_once_with(
          'CreateInvocation', {
              'invocation': {
                  'producerResource':
                      '//test-swarming.appspot.com/tasks/task001'
              },
              'requestId': '00000000-0000-0000-0000-000000000000',
              'invocationId': 'task:test-swarming.appspot.com:task001'
          }, mock.ANY)

  def test_finalize_invocation_success(self):
    with mock.patch('server.resultdb._call_resultdb_recorder_api') as mock_call:
      resultdb.finalize_invocation('task001', True)
      mock_call.assert_called_once_with('FinalizeInvocation', {
          'name': 'task:test-swarming.appspot.com:task001',
          'interrupted': True
      })

  def test_finalize_invocation_invalide_argument(self):
    with mock.patch('server.resultdb._call_resultdb_recorder_api') as mock_call:
      mock_call.side_effect = net.Error(
          msg='error',
          status_code=400,
          response='error',
          headers={'X-Prpc-Grpc-Code': '3'})
      resultdb.finalize_invocation('task001', True)
      mock_call.assert_called_once_with('FinalizeInvocation', {
          'name': 'task:test-swarming.appspot.com:task001',
          'interrupted': True
      })

  def test_finalize_invocation_failed(self):
    with mock.patch('server.resultdb._call_resultdb_recorder_api') as mock_call:
      mock_call.side_effect = Exception('failed')
      with self.assertRaises(Exception):
        resultdb.finalize_invocation('task001', True)
      mock_call.assert_called_once_with('FinalizeInvocation', {
          'name': 'task:test-swarming.appspot.com:task001',
          'interrupted': True
      })

  def test_call_resultdb_recorder_api(self):
    with mock.patch('server.config.settings') as mock_settings, mock.patch(
        'components.net.json_request') as mock_json_request:
      mock_settings.return_value = config_pb2.SettingsCfg(
          resultdb=config_pb2.ResultDBSettings(
              server='https://results.api.cr.dev'),)
      mock_json_request.return_value = {}

      resultdb._call_resultdb_recorder_api('FinalizeInvocation', {})

      mock_settings.assert_called_once()
      mock_json_request.assert_called_once()


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  logging.basicConfig(
      level=logging.DEBUG if '-v' in sys.argv else logging.CRITICAL)
  unittest.main()
