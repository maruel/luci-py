# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.
"""Functions to communicate with ResultDB for swarming tasks."""

import logging
import uuid

from google.appengine.api import app_identity
from google.appengine.ext import ndb

from components import net
from components import prpc
from components import utils

from server import config


@ndb.tasklet
def create_invocation_async(task_run_id):
  """This is wrapper for CreateInvocation API.

  Returns:
    update-token for created invocation.
  """
  hostname = app_identity.get_default_version_hostname()
  response_headers = {}
  yield _call_resultdb_recorder_api_async(
      'CreateInvocation', {
          'requestId': str(uuid.uuid4()),
          'invocationId': _get_invocation_id(task_run_id),
          'invocation': {
              'producerResource': '//%s/tasks/%s' % (hostname, task_run_id),
          }
      },
      response_headers=response_headers)

  raise ndb.Return(response_headers.get('update-token'))


@ndb.tasklet
def finalize_invocation_async(task_run_id):
  """This is wrapper for FinalizeInvocation API."""

  try:
    invocation_name = get_invocation_name(task_run_id)
    yield _call_resultdb_recorder_api_async('FinalizeInvocation', {
        'name': invocation_name,
    })
  except net.Error:
    logging.exception('Failed to finalize invocation %s', invocation_name)


def get_invocation_name(task_run_id):
  return 'invocations/%s' % _get_invocation_id(task_run_id)


### Private code


def _get_invocation_id(task_run_id):
  hostname = app_identity.get_default_version_hostname()
  return 'task:%s:%s' % (hostname, task_run_id)


@ndb.tasklet
def _call_resultdb_recorder_api_async(method, request, response_headers=None):
  cfg = config.settings()
  rdb_url = cfg.resultdb.server
  assert rdb_url, 'ResultDB integration is not configured'
  utils.validate_root_service_url(rdb_url)

  # See Recoder API for ResultDB in
  # https://chromium.googlesource.com/infra/luci/luci-go/+/HEAD/resultdb/proto/rpc/v1/recorder.proto
  # But beware that proto JSON serialization uses camelCase, not snake_case.
  yield net.json_request_async(
      url='%s/prpc/luci.resultdb.rpc.v1.Recorder/%s' % (rdb_url, method),
      method='POST',
      payload=request,
      scopes=[net.EMAIL_SCOPE],
      response_headers=response_headers)
