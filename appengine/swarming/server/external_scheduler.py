# Copyright 2018 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Helper functions for interacting with an external scheduler."""

import logging

from components import utils
from components import datastore_utils

from components.prpc import client

from google.appengine.ext import ndb
from google.protobuf import json_format

from proto.api import plugin_pb2
from proto.api import plugin_prpc_pb2
from proto.api import swarming_pb2

from server import pools_config
from server import task_queues


class ExternalSchedulerException(Exception):
  """Raised when an external-scheduler related error occurs."""


def _get_client(address):
  """Get a prpc client instance for given address."""
  return client.Client(
      address, plugin_prpc_pb2.ExternalSchedulerServiceDescription,
      insecure=utils.is_local_dev_server())


def _creds():
  """Get the correct credentials argument for this environment."""
  return (None if utils.is_local_dev_server() else
          client.service_account_credentials())


def _bot_pool_cfg(bot_dimensions):
  """Retrieves the PoolConfig for a bot.

  Arguments:
  - bot_dimensions: The dimensions of the bot as a dictionary in
          {string key: list of string values} format.

  Returns:
    PoolConfig for the bot if it exists, or None otherwise.
  """
  pools = bot_dimensions.get(u'pool')
  if not pools:
    return None
  if len(pools) == 1:
    return pools_config.get_pool_config(pools[0])
  else:
    logging.warning('Bot with dimensions %s was found to be in multiple '
                    'pools. Unable to determine pool config.',
                    bot_dimensions)

  return None


def _config_for_dimensions(pool_cfg, dimensions_flat):
  """Determines the external scheduler for pool config and dimension set."""
  if not pool_cfg or not pool_cfg.external_schedulers:
    return None
  for e in pool_cfg.external_schedulers:
    if e.enabled and e.dimensions.issubset(dimensions_flat):
      return e
  return None


### Public API.


def config_for_bot(bot_dimensions):
  """Retrieves the ExternalSchedulerConfig for this bot, if any.

  Arguments:
  - bot_dimensions: The dimensions of the bot as a dictionary in
          {string key: list of string values} format.

  Returns:
    pools_config.ExternalSchedulerConfig for external scheduler to use for
    this bot, if it exists, or None otherwise.
  """
  pool_cfg = _bot_pool_cfg(bot_dimensions)
  bot_dimensions_flat = set(task_queues.dimensions_to_flat(bot_dimensions))
  return _config_for_dimensions(pool_cfg, bot_dimensions_flat)


def config_for_task(request):
  """Retrieves the ExternalSchedulerConfig for this task request, if any.

  Arguments:
    request: a task_request.TaskRequest instance.

  Returns:
    pools_config.ExternalSchedulerConfig for external scheduler to use for
    this bot, if it exists, or None otherwise.
  """
  s0 = request.task_slice(0)
  pool = s0.properties.pool
  if not pool:
    return None
  pool_cfg = pools_config.get_pool_config(pool)
  if not pool_cfg or not pool_cfg.external_schedulers:
    return None

  # Determine the dimension intersection across all task slices.
  common_dimensions = set(
      task_queues.dimensions_to_flat(s0.properties.dimensions))
  for i in range(1, request.num_task_slices):
    s = request.task_slice(i)
    common_dimensions.intersection_update(
        task_queues.dimensions_to_flat(s.properties.dimensions))

  return _config_for_dimensions(pool_cfg, common_dimensions)


def assign_task(es_cfg, bot_dimensions):
  """Calls external scheduler for a single idle bot with given dimensions.

  Arguments:
    es_cfg: pools_config.ExternalSchedulerConfig instance.
    bot_dimensions: dimensions {string key: list of string values}

  Returns:
    (Task id string, slice number) tuple or (None, None) if no task
    to assign.
  """
  bot_id = bot_dimensions[u'id'][0]
  logging.debug('Using external scheduler address: %s id: %s for bot %s',
                es_cfg.address, es_cfg.id, bot_id)

  req = plugin_pb2.AssignTasksRequest()

  idle_bot = req.idle_bots.add()
  idle_bot.bot_id = bot_id
  idle_bot.dimensions.extend(task_queues.dimensions_to_flat(bot_dimensions))

  req.scheduler_id = es_cfg.id
  req.time.GetCurrentTime()

  c = _get_client(es_cfg.address)

  # TODO(akeshet): Catch or handle errors appropriately.
  resp = c.AssignTasks(req, credentials=_creds())

  if not resp or not resp.assignments:
    return None, None

  assert len(resp.assignments) == 1
  assert resp.assignments[0].bot_id == bot_id

  return resp.assignments[0].task_id, resp.assignments[0].slice_number


def notify_requests(es_cfg, requests, use_tq, is_callback, use_pq=False):
  """Calls external scheduler to notify it of a task state.

  Arguments:
    - es_cfg: pools_config.ExternalSchedulerConfig for external scheduler to
        notify.
    - requests:
      A list of (task_request.TaskRequest,
                 task_result.TaskResultSummary or task_result.TaskRunResult)
      tuples.
    - use_tq: If true, make this call on a task queue (within the current
              datastore transaction).
    - is_callback: If true, indicates that this notification was in response
                   to a external-scheduler-requested callback. This is for
                   diagnostic purposes.
    - use_pq: TODO(lxn) add comment

  Returns: Nothing.
  """
  logging.debug(
      'notify_requests(es_cfg=(%s,%s), requests=%s, use_tq=%s, '
      'is_callback=%s)',
      es_cfg.address, es_cfg.id, [r.task_id for r, _ in requests], use_tq,
      is_callback)

  req = plugin_pb2.NotifyTasksRequest()
  req.is_callback = is_callback

  for request, result_summary in requests:
    item = req.notifications.add()
    # TODO(akeshet): This time should possibly come from the read time from
    # datastore, rather than the local server clock.
    item.time.FromDatetime(utils.utcnow())
    item.task.id = request.task_id
    item.task.tags.extend(request.tags)
    item.task.enqueued_time.FromDatetime(request.created_ts)
    for i in range(request.num_task_slices):
      s = request.task_slice(i)
      flat_dimensions = task_queues.dimensions_to_flat(s.properties.dimensions)
      s_pb = item.task.slices.add()
      s_pb.dimensions.extend(flat_dimensions)

    res = swarming_pb2.TaskResult()
    result_summary.to_proto(res)
    item.task.state = res.state
    if result_summary.bot_id:
      # TODO(akeshet): We should only actually set this is state is running.
      item.task.bot_id = result_summary.bot_id

  req.scheduler_id = es_cfg.id

  if use_tq:
    request_json = json_format.MessageToJson(req)
    enqueued = utils.enqueue_task(
      '/internal/taskqueue/important/external_scheduler/notify-tasks',
      'es-notify-tasks',
      params={'es_host': es_cfg.address, 'request_json': request_json},
      transactional=ndb.in_transaction())
    if not enqueued:
      raise datastore_utils.CommitError('Failed to enqueue task')
  elif use_pq:
    req_enqueued = utils.enqueue_task(
      '',
      'es-notify-requests',
      payload=request_json,
      method='PULL',
      tag=es_cfg.address)
    if not req_enqueued:
      raise datastore_utils.CommitError('Failed to enqueue task')
    # TOOD(lxn): add comment
    job_enqueued = utils.enqueue_task(
      '/internal/taskqueue/important/external_scheduler/es-notify-tasks',
      'es-notify-tasks',
      params={'es_host': es_cfg.address},
      transactional=ndb.in_transaction())
    if not job_enqueued:
       logging.info('Failed to add a notify-task for request: %r', request_json)
  else:
    # Ignore return value, the response proto is empty.
    notify_request_now(es_cfg.address, req)


def notify_request_now(es_host, proto):
  """Calls external scheduler's NotifyTask endpoint immediately.

  Arguments:
    es_host: Address of external scheduler to use.
    proto: plugin_pb2.NotifyTasksRequest instance to call with.
  """
  c = _get_client(es_host)
  return c.NotifyTasks(proto, credentials=_creds())


def notify_request_batch(es_host):
  """Leases the notification-tasks from es-notify-requests. Combines tasks
     into HTTP requests by their scheduler ID.

    Arguments:
      es_host: Address of external scheduler to use.
  """
  tasks = utils.lease_tasks('es-notify-requests', 60, 100, tag=es_host)
  requests = collections.defaultdict(object)
  delete_tasks = collections.defaultdict(list)
  for task in tasks:
    notify_task = plugin_pb2.NotifyTasksRequest(is_callback=False)
    json_format.Parse(task.payload, notify_task)
    if notify_task.scheduler_id not in requests.keys():
      requests[notify_task.scheduler_id] = notify_task
      delete_tasks[notify_task.scheduler_id] = [task]
      continue
    requests[notify_task.scheduler_id].notifications.extend(
        notify_task.notifications)
    delete_tasks[notify_task.scheduler_id].append(task)

  c = _get_client(es_host)
  for k, v in requests.iteritems():
    try:
      c.NotifyTasks(v, credentials=_creds())
      utils.delete_tasks('es-notify-requests', delete_tasks[k])
    except:
      # We do not delete those tasks if failed, but add one notify-task back.
      utils.enqueue_task(
          '/internal/taskqueue/important/external_scheduler/es-notify-jobs',
          'es-notify-jobs',
          params={'es_host': es_host},
          transactional=ndb.in_transaction())
  return


def get_cancellations(es_cfg):
  """Calls external scheduler and returns task cancellations."""
  req = plugin_pb2.GetCancellationsRequest()
  req.scheduler_id = es_cfg.id
  c = _get_client(es_cfg.address)
  resp = c.GetCancellations(req, credentials=_creds())
  return resp.cancellations


def get_callbacks(es_cfg):
  """Calls external scheduler and returns callback task ids."""
  req = plugin_pb2.GetCallbacksRequest()
  req.scheduler_id = es_cfg.id
  c = _get_client(es_cfg.address)
  resp = c.GetCallbacks(req, credentials=_creds())
  return resp.task_ids
