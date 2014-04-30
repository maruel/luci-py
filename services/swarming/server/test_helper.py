# Copyright 2013 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""Some helper test functions."""

import datetime

from google.appengine.ext import ndb

from common import test_request_message
from server import result_helper
from server import task_common
from server import task_glue
from server import task_result
from server import task_shard_to_run
from server import task_scheduler
from server import test_request
from server import test_runner

# pylint: disable=W0212


# The default root for all configs in a test request. The index value of the
# config is appended to the end to make the full default name.
REQUEST_MESSAGE_CONFIG_NAME_ROOT = 'c1'

# The default name for a TestRequest.
REQUEST_MESSAGE_TEST_CASE_NAME = 'tc'


def _CreateRunner(request, config_name):
  """Create a basic runner.

  Args:
    request: The TestRequest that owns this runner.
    config_name: The config name for the runner.

  Returns:
    The newly created runner.
  """
  runner = test_runner.TestRunner(
      request=request.key,
      config_name=config_name,
      config_hash=request.GetConfigurationDimensionHash(config_name))
  runner.put()

  request.runner_keys.append(runner.key)
  request.put()

  return runner


def GetRequestMessage(request_name=REQUEST_MESSAGE_TEST_CASE_NAME,
                      config_name_root=REQUEST_MESSAGE_CONFIG_NAME_ROOT,
                      num_instances=1,
                      env_vars=None,
                      restart_on_failure=False,
                      platform='win-xp',
                      priority=10,
                      num_configs=1,
                      requestor=None):
  """Return a properly formatted request message text.

  Args:
    request_name: The name of the test request.
    config_name_root: The base name of each config (it will have the instance
        number appended to it).
    num_instances: The number of instance for the given config.
    env_vars: A dictionary of environment variables for the request.
    restart_on_failure: Identifies if the slave should be restarted if any
        of its tests fail.
    platform: The os to require in the test's configuration.
    priority: The priority given to this request.
    num_configs: The number of configs to have in the request message.

  Returns:
    A properly formatted request message text.
  """
  tests = [
    test_request_message.TestObject(test_name='t1', action=['ignore-me.exe']),
  ]
  configurations = [
    test_request_message.TestConfiguration(
        config_name=config_name_root + '_' + str(i),
        dimensions=dict(os=platform, cpu='Unknown', browser='Unknown'),
        num_instances=num_instances,
        priority=priority)
    for i in range(num_configs)
  ]
  request = test_request_message.TestCase(
      restart_on_failure=restart_on_failure,
      requestor=requestor,
      test_case_name=request_name,
      configurations=configurations,
      data=[('http://b.ina.ry/files2.zip', 'files2.zip')],
      env_vars=env_vars,
      tests=tests)
  return test_request_message.Stringize(request, json_readable=True)


def CreateRunner(config_name=None, machine_id=None,
                 ran_successfully=None, exit_codes=None, started=None,
                 ended=None, requestor=None, results=None):
  """Creates entities to represent a new task request and a bot running it.

  For the old DB, it's a TestRequest and TestRunner pair
  For the new DB, it's a TaskRequest and friends.

  The entity may be in a pending, running or completed state.

  Args:
    config_name: The config name for the runner.
    machine_id: The machine id for the runner. Also, if this is given the
      runner is marked as having started.
    ran_succesfully: True if the runner ran successfully.
    exit_codes: The exit codes for the runner. Also, if this is given the
      runner is marked as having finished.
    started: timedelta from .created to when the task execution started.
    ended: timedelta from .started to when the bot completed the task.
    requestor: string representing the user name that requested the task.
    results: string that represents stdout the bot sent back.

  Returns:
    The pending runner created.
  """
  config_name = config_name or (REQUEST_MESSAGE_CONFIG_NAME_ROOT + '_0')
  request_message = GetRequestMessage(requestor=requestor)
  if task_glue.USE_OLD_API:
    request = test_request.TestRequest(
        message=request_message,
        name=REQUEST_MESSAGE_TEST_CASE_NAME)
    request.put()

    runner = _CreateRunner(request, config_name)
    runner.config_instance_index = 0
    runner.num_config_instances = 1
    runner.requestor = requestor

    if machine_id:
      runner.machine_id = machine_id
      runner.started = datetime.datetime.utcnow()
      runner.ping = runner.started

    if ran_successfully:
      runner.ran_successfully = ran_successfully

    if exit_codes:
      runner.done = True
      runner.ended = datetime.datetime.utcnow()
      runner.exit_codes = exit_codes

    if started:
      runner.started = runner.created + started

    if ended:
      runner.ended = runner.started + ended

    if results:
      results_obj = result_helper.StoreResults(results)
      runner.results_reference = results_obj.key

    runner.put()
    return runner

  data = task_glue._convert_test_case(request_message)
  request, shard_runs = task_scheduler.new_request(data)
  shard_to_run_key = shard_runs[0].key
  # This is in running state. Pending state is not supported here.
  task_shard_to_run.reap_shard_to_run(shard_to_run_key)

  machine_id = machine_id or 'localhost'
  shard_result = task_result.new_shard_result(shard_to_run_key, 1, machine_id)
  if started:
    shard_result.started_ts += started
  if ended:
    shard_result.completed_ts = shard_result.started_ts + ended

  if ran_successfully or exit_codes:
    data = {
      'exit_codes': exit_codes or [0],
    }
    task_scheduler.bot_update_task(shard_result.key, data, machine_id)

  # Call it manually because at this level, there is no visibility for the
  # taskqueue.
  task_result._task_update_result_summary(request.key.integer_id())

  # Returns a TaskShardResult.
  return shard_result


def CreateRequest(num_instances):
  """Creates a basic request with the specified number of runners.

  Args:
    num_instances: The number of runner instances to give this request.

  Returns:
    The newly created request.
  """
  request = test_request.TestRequest(message=GetRequestMessage(),
                                     name=REQUEST_MESSAGE_TEST_CASE_NAME)
  request.put()

  for i in range(num_instances):
    runner = _CreateRunner(request, REQUEST_MESSAGE_CONFIG_NAME_ROOT + '_0')
    runner.config_instance_index = i
    runner.num_config_instances = num_instances
    runner.put()

  return request


def mock_now(test, now):
  """Mocks utcnow() and ndb properties.

  In particular handles when auto_now and auto_now_add are used.

  To be used in tests only.
  """
  test.mock(task_common, 'utcnow', lambda: now)
  test.mock(ndb.DateTimeProperty, '_now', lambda _: now)
  test.mock(ndb.DateProperty, '_now', lambda _: now.date())
