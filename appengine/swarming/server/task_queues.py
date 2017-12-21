# Copyright 2017 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Ambient task queues generated from the actual load.

This means that the task queues are deduced by the actual load, they are never
explicitly defined. They are eventually deleted by a cron job once no incoming
task with the exact set of dimensions is triggered anymore.

Used to optimize scheduling.

    +---------+
    |BotRoot  |                                                bot_management.py
    |id=bot_id|
    +---------+
        |
        +------+
        |      |
        |      v
        |  +-------------+
        |  |BotDimensions|
        |  |id=1         |
        |  +-------------+
        |
        +---------------- ... ----+
        |                         |
        v                         v
    +-------------------+     +-------------------+
    |BotTaskDimensions  | ... |BotTaskDimensions  |
    |id=<dimension_hash>| ... |id=<dimension_hash>|
    +-------------------+     +-------------------+

    +-------Root------------+
    |TaskDimensionsRoot     |  (not stored)
    |id=<pool:foo or id:foo>|
    +-----------------------+
        |
        +---------------- ... -------+
        |                            |
        v                            v
    +----------------------+     +----------------------+
    |TaskDimensions        | ... |TaskDimensions        |
    |  +-----------------+ | ... |  +-----------------+ |
    |  |TaskDimensionsSet| |     |  |TaskDimensionsSet| |
    |  +-----------------+ |     |  +-----------------+ |
    |id=<dimension_hash>   |     |id=<dimension_hash>   |
    +----------------------+     +----------------------+
"""

import datetime
import hashlib
import json
import logging
import random
import struct
import time

from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.ext import ndb

from components import datastore_utils
from components import utils
from server import bot_management
from server import task_pack


# Frequency at which these entities must be refreshed. This value is a trade off
# between constantly updating BotTaskDimensions and TaskDimensions vs keeping
# them alive for longer than necessary, causing unnecessary queries in
# get_queues() users.
#
# The 10 minutes delta is from assert_task() which advance the timer by a random
# value to up 10 minutes early.
_ADVANCE = datetime.timedelta(hours=1, minutes=10)


class Error(Exception):
  pass


### Models.


class BotDimensions(ndb.Model):
  """Notes the current valid bot dimensions.

  Parent is BotRoot.
  Key id is 1.

  This is redundant from BotEvents but it is leveraged to quickly assert if
  _rebuild_bot_cache_async() must be called or not.
  """
  # 'key:value' strings. This is stored to enable the removal of stale entities
  # when the bot changes its dimensions.
  dimensions_flat = ndb.StringProperty(repeated=True)

  def _pre_put_hook(self):
    super(BotDimensions, self)._pre_put_hook()
    if self.key.integer_id() != 1:
      raise datastore_errors.BadValueError(
          '%s.key.id must be 1' % self.__class__.__name__)
    _validate_dimensions_flat(self)


class BotTaskDimensions(ndb.Model):
  """Stores the precalculated hashes for this bot.

  Parent is BotRoot.
  Key id is <dimensions_hash>. It is guaranteed to fit 32 bits.

  This hash could be conflicting different properties set, but this doesn't
  matter at this level because disambiguation is done in TaskDimensions
  entities.

  The number of stored entities is:
    <number of bots> x <TaskDimensions each bot support>

  The actual number if a direct function of the variety of the TaskDimensions.
  """
  # Validity time, at which this entity should be considered irrelevant.
  valid_until_ts = ndb.DateTimeProperty()
  # 'key:value' strings. This is stored to enable the removal of stale entities
  # when the bot changes its dimensions.
  dimensions_flat = ndb.StringProperty(repeated=True, indexed=False)

  def is_valid(self, bot_dimensions):
    """Returns true if this entity is still valid for the bot dimensions."""
    for i in self.dimensions_flat:
      k, v = i.split(':', 1)
      if v not in bot_dimensions.get(k, []):
        return False
    return True

  def _pre_put_hook(self):
    super(BotTaskDimensions, self)._pre_put_hook()
    if not self.valid_until_ts:
      raise datastore_errors.BadValueError(
          '%s.valid_until_ts is required' % self.__class__.__name__)
    _validate_dimensions_flat(self)


class TaskDimensionsRoot(ndb.Model):
  """Ghost root entity to group kinds of tasks to a common root.

  This root entity is not stored in the DB.

  id is either 'id:<value>' or 'pool:<value>'. For a request dimensions set that
  specifies both keys, TaskDimensions is listed under 'id:<value>'.
  """
  pass


class TaskDimensionsSet(ndb.Model):
  """Embedded struct to store a set of dimensions.

  This entity is not stored, it is contained inside TaskDimensions.sets.
  """
  # Validity time, at which this entity should be considered irrelevant.
  # Entities with valid_until_ts in the past are considered inactive and are not
  # used. valid_until_ts is set in assert_task() to "TaskRequest.expiration_ts +
  # _ADVANCE". It is updated when an assert_task() call sees that valid_until_ts
  # becomes lower than TaskRequest.expiration_ts for a later task. This enables
  # not updating the entity too frequently, at the cost of keeping a dead queue
  # "alive" for a bit longer than strictly necessary.
  valid_until_ts = ndb.DateTimeProperty()

  # 'key:value' strings. This is stored to enable match_bot(). This is important
  # as the dimensions_hash in TaskDimensions can be colliding, so the exact list
  # is needed to ensure we are comparing the expected dimensions.
  dimensions_flat = ndb.StringProperty(repeated=True, indexed=False)

  def match_bot(self, bot_dimensions):
    """Returns True if this bot can run this request dimensions set."""
    for d in self.dimensions_flat:
      key, value = d.split(':', 1)
      if value not in bot_dimensions.get(key, []):
        return False
    return True

  def _pre_put_hook(self):
    super(TaskDimensionsSet, self)._pre_put_hook()
    if not self.valid_until_ts:
      raise datastore_errors.BadValueError(
          '%s.valid_until_ts is required' % self.__class__.__name__)
    _validate_dimensions_flat(self)


class TaskDimensions(ndb.Model):
  """List dimensions for each kind of task.

  Parent is TaskDimensionsRoot
  Key id is <dimensions_hash>. It is guaranteed to fit 32 bits.

  A single dimensions_hash may represent multiple independent queues in a single
  root. This is because the hash is very compressed (32 bits). This is handled
  specifically here by having one set of TaskDimensionsSet per 'set'.

  The worst case of having hash collision is unneeded scanning for unrelated
  tasks in get_queues(). This is bad but not the end of the world.

  It is only a function of the number of different tasks, so it is not expected
  to be very large, only in the few hundreds. The exception is when one task per
  bot is triggered, which leads to have at <number of bots> TaskDimensions
  entities.
  """
  # Lowest value of TaskDimensionsSet.valid_until_ts. See its documentation for
  # more details.
  valid_until_ts = ndb.ComputedProperty(
      lambda self: self._calc_valid_until_ts())

  # One or multiple sets of request dimensions this dimensions_hash represents.
  sets = ndb.LocalStructuredProperty(TaskDimensionsSet, repeated=True)

  def assert_request(self, now, valid_until_ts, dimensions_flat):
    """Updates this entity to assert this dimensions_flat is supported.

    Returns:
      True if the entity was updated; it can be that a TaskDimensionsSet was
      added, updated or a stale one was removed.
    """
    s = self._match_request_flat(dimensions_flat)
    if not s:
      self.sets.append(
          TaskDimensionsSet(
              valid_until_ts=valid_until_ts, dimensions_flat=dimensions_flat))
      self.sets = [s for s in self.sets if s.valid_until_ts >= now]
      return True
    if s.valid_until_ts < valid_until_ts:
      s.valid_until_ts = valid_until_ts
      self.sets = [s for s in self.sets if s.valid_until_ts >= now]
      return True
    # It was updated already, skip storing again.
    old = len(self.sets)
    self.sets = [s for s in self.sets if s.valid_until_ts >= now]
    return len(self.sets) != old

  def match_request(self, dimensions):
    """Confirms that this instance actually stores this set."""
    return self._match_request_flat(
        u'%s:%s' % (k, v) for k, v in dimensions.iteritems())

  def match_bot(self, bot_dimensions):
    """Returns the TaskDimensionsSet that matches this bot_dimensions, if any.
    """
    for s in self.sets:
      if s.match_bot(bot_dimensions):
        return s

  def _match_request_flat(self, dimensions_flat):
    d = frozenset(dimensions_flat)
    for s in self.sets:
      if not d.difference(s.dimensions_flat):
        return s

  def _calc_valid_until_ts(self):
    if not self.sets:
      raise datastore_errors.BadValueError(
          '%s.sets must be specified' % self.__class__.__name__)
    return min(s.valid_until_ts for s in self.sets)

  def _pre_put_hook(self):
    super(TaskDimensions, self)._pre_put_hook()
    sets = set()
    for s in self.sets:
      s._pre_put_hook()
      sets.add('\000'.join(s.dimensions_flat))
    if len(sets) != len(self.sets):
      # Make sure there's no duplicate TaskDimensionsSet.
      raise datastore_errors.BadValueError(
          '%s.sets must all be unique' % self.__class__.__name__)


### Private APIs.


def _validate_dimensions_flat(obj):
  """Validates obj.dimensions_flat; throws BadValueError if invalid."""
  if not obj.dimensions_flat:
    raise datastore_errors.BadValueError(
        '%s.dimensions_flat is empty' % obj.__class__.__name__)
  if len(obj.dimensions_flat) != len(set(obj.dimensions_flat)):
    raise datastore_errors.BadValueError(
        '%s.dimensions_flat has duplicate entries' % obj.__class__.__name__)
  if sorted(obj.dimensions_flat) != obj.dimensions_flat:
    raise datastore_errors.BadValueError(
        '%s.dimensions_flat must be sorted' % obj.__class__.__name__)


def _flatten_bot_dimensions(bot_dimensions):
  dimensions_flat = []
  for k, values in bot_dimensions.iteritems():
    for v in values:
      dimensions_flat.append(u'%s:%s' % (k, v))
  return sorted(dimensions_flat)


def _get_task_queries_for_bot(bot_dimensions):
  """Returns all the ndb.Query for TaskDimensions relevant for this bot."""
  opts = ndb.QueryOptions(batch_size=100, deadline=15)
  ancestors = [ndb.Key(TaskDimensionsRoot, u'id:' + bot_dimensions[u'id'][0])]
  for pool in bot_dimensions['pool']:
    ancestors.append(ndb.Key(TaskDimensionsRoot, u'pool:' + pool))
  # These are consistent queries because they use an ancestor. The old entries
  # are removed by cron job /internal/cron/task_queues_tidy triggered every N
  # minutes (see cron.yaml).
  return [
      TaskDimensions.query(default_options=opts, ancestor=a)
      for a in ancestors
  ]


def _cap_futures(futures):
  """Limits the number of on-going ndb.Future to 50.

  Having too many on-going RPCs may lead to memory exhaustion.
  """
  out = []
  while len(futures) > 50:
    # Give the event loop some time to run tasks.
    r = ndb.eventloop.run0()
    if r is not None:
      time.sleep(r)
    done = []
    for f in futures:
      if f.done():
        out.append(f.get_result())
        done.append(f)
    futures.difference_update(done)
  return out


def _flush_futures(futures):
  return [f.get_result() for f in futures]


@ndb.tasklet
def _rebuild_bot_cache_async(bot_dimensions, bot_root_key):
  """Rebuilds the BotTaskDimensions cache for a single bot.

  This is done by a linear scan for all the TaskDimensions under the
  TaskDimensionsRoot entities with key id 'id:<bot_id>' and 'pool:<pool>', for
  each pool exposed by the bot. Only the TaskDimensions with TaskDimensionsRoot
  id with bot's id or the bot's pool are queried, not *all* TaskDimensions.

  Normally bots are in one or an handful of pools so the number of queries
  should be relatively low. This is all ancestor queries, so they are
  consistent.

  Runtime expectation: the scale is low enough that it can be run inline with
  the bot's poll request.

  The update completes with BotDimensions being updated and memcache entry for
  get_queues() updated.
  """
  now = utils.utcnow()
  bot_id = bot_dimensions[u'id'][0]
  matches = []
  cleaned = [0]
  try:
    # First delete any BotTaskDimensions that do not match the current
    # dimensions.
    @ndb.tasklet
    def _handle_bot(i):
      if not i.is_valid(bot_dimensions):
        # This BotTaskDimensions doesn't match bot_dimensions anymore, remove.
        yield i.key.delete_async()
        cleaned[0] += 1

    q = BotTaskDimensions.query(ancestor=bot_root_key)
    futures = [q.map_async(_handle_bot, batch_size=64)]

    # The expected total number of TaskDimensions is in the tens or few
    # hundreds, as it depends on all the kinds of different task dimensions that
    # this bot could run that are ACTIVE queues, e.g.
    # TaskDimensions.valid_until_ts is in the future.
    # TODO(maruel): Run the queries in parallel if it becomes an issue, e.g.
    # datastore_utils.incremental_map().
    @ndb.tasklet
    def _handle_task_dimensions(task_dimensions):
      s = task_dimensions.match_bot(bot_dimensions)
      if s and s.valid_until_ts >= now:
        # Stale TaskDimensionsSet.
        dimensions_hash = task_dimensions.key.integer_id()
        # Reuse TaskDimensionsSet.valid_until_ts.
        obj = BotTaskDimensions(
            id=dimensions_hash, parent=bot_root_key,
            valid_until_ts=s.valid_until_ts,
            dimensions_flat=s.dimensions_flat)
        yield obj.put_async()
        matches.append(dimensions_hash)

    for q in _get_task_queries_for_bot(bot_dimensions):
      futures.append(q.map_async(_handle_task_dimensions, batch_size=64))

    # Wait for all of them before the next step.
    for f in futures:
      yield f

    # Seal the fact that it has been updated.
    obj = BotDimensions(
        id=1, parent=bot_root_key,
        dimensions_flat=_flatten_bot_dimensions(bot_dimensions))
    # Do these steps in order.
    yield obj.put_async()
    yield ndb.get_context().memcache_set(
        bot_id, sorted(matches), namespace='task_queues')
  finally:
    logging.debug(
        '_rebuild_bot_cache_async(%s) in %.3fs. Registered for %d queues; '
        'cleaned %d',
        bot_id, (utils.utcnow()-now).total_seconds(), len(matches), cleaned[0])


def _get_task_dims_key(dimensions_hash, dimensions):
  if u'id' in dimensions:
    return ndb.Key(
        TaskDimensionsRoot, u'id:%s' % dimensions['id'],
        TaskDimensions, dimensions_hash)
  return ndb.Key(
      TaskDimensionsRoot, u'pool:%s' % dimensions['pool'],
      TaskDimensions, dimensions_hash)


def _hash_data(data):
  """Returns a 32 bits non-zero hash."""
  assert isinstance(data, str), repr(data)
  digest = hashlib.md5(data).digest()
  # Note that 'L' means C++ unsigned long which is (usually) 32 bits and
  # python's int is 64 bits.
  return int(struct.unpack('<L', digest[:4])[0]) or 1


@ndb.tasklet
def _remove_old_entity_async(key, now):
  """Removes a stale TaskDimensions or BotTaskDimensions instance.

  Returns:
    key if it was deleted.
  """
  obj = key.get()
  if not obj or obj.valid_until_ts >= now:
    raise ndb.Return(None)

  @ndb.tasklet
  def tx():
    obj = yield key.get_async()
    if obj and obj.valid_until_ts < now:
      yield key.delete_async()
      raise ndb.Return(key)

  res = yield datastore_utils.transaction_async(
      tx, propagation=ndb.TransactionOptions.INDEPENDENT)
  raise ndb.Return(res)


def _yield_BotTaskDimensions_keys(dimensions_hash, dimensions_flat):
  """Yields all the BotTaskDimensions ndb.Key for the bots that correspond to
  these task request dimensions.
  """
  opts = ndb.QueryOptions(batch_size=100, keys_only=True, deadline=15)
  q = BotDimensions.query(default_options=opts)
  for d in dimensions_flat:
    q = q.filter(BotDimensions.dimensions_flat == d)

  # This is slightly costly but helps figuring out performance issues. Since
  # this is in a task queue, this is acceptable even if it may slightly delay
  # task execution on fresh new task dimension.
  logging.debug(
      '_yield_BotTaskDimensions_keys(%d, %s) = %d BotDimensions',
      dimensions_hash, dimensions_flat, q.count())

  for bot_info_key in q:
    yield ndb.Key(
        BotTaskDimensions, dimensions_hash, parent=bot_info_key.parent())


@ndb.tasklet
def _refresh_BotTaskDimensions(
    bot_task_key, dimensions_flat, now, valid_until_ts):
  """Creates or refreshes a BotTaskDimensions.

  Arguments:
  - bot_task_key: ndb.Key to a BotTaskDimensions
  - dimensions_flat: list of '<key>:<value>' for the task request dimensions
  - now: datetime.datetime of 'now'
  - valid_until_ts: datetime.datetime determines until when this
    dimensions_flat should remain valid.

  Returns:
    True if the entity was updated, False if no-op.
  """
  bot_task = yield bot_task_key.get_async()
  # Play safe. If the BotTaskDimensions was close to be ignored, refresh the
  # memcache entry.
  cutoff = now - datetime.timedelta(minutes=1)
  need_memcache_clear = True
  need_db_store = True
  if bot_task and set(bot_task.dimensions_flat) == set(dimensions_flat):
    need_memcache_clear = bot_task.valid_until_ts < cutoff
    # Skip storing if the validity period was already updated.
    need_db_store = bot_task.valid_until_ts < valid_until_ts

  if need_db_store:
    yield BotTaskDimensions(
        key=bot_task_key, valid_until_ts=valid_until_ts,
        dimensions_flat=dimensions_flat).put_async()
  if need_memcache_clear:
    bot_id = bot_task_key.parent().string_id()
    yield ndb.get_context().memcache_delete(bot_id, namespace='task_queues')
  raise ndb.Return(need_db_store)


### Public APIs.


def hash_dimensions(dimensions):
  """Returns a 32 bits int that is a hash of the request dimensions specified.

  Arguments:
    dimensions: dict(str, str)

  The return value is guaranteed to be a non-zero int so it can be used as a key
  id in a ndb.Key.
  """
  # This horrible code is the product of micro benchmarks.
  data = ''
  for k, v in sorted(dimensions.items()):
    data += k.encode('utf8')
    data += '\000'
    data += v.encode('utf8')
    data += '\000'
  return _hash_data(data)


@ndb.tasklet
def assert_bot_async(bot_dimensions):
  """Prepares BotTaskDimensions entities as needed.

  Coupled with assert_task(), enables get_queues() to work by by knowing which
  TaskDimensions applies to this bot.
  """
  assert len(bot_dimensions[u'id']) == 1, bot_dimensions
  # Check if the bot dimensions changed since last _rebuild_bot_cache_async()
  # call.
  bot_root_key = bot_management.get_root_key(bot_dimensions[u'id'][0])
  obj = yield ndb.Key(BotDimensions, 1, parent=bot_root_key).get_async()
  if obj and obj.dimensions_flat == _flatten_bot_dimensions(bot_dimensions):
    # Cache hit, no need to look further.
    raise ndb.Return(None)

  yield _rebuild_bot_cache_async(bot_dimensions, bot_root_key)


def cleanup_after_bot(bot_id):
  """Removes all BotDimensions and BotTaskDimensions for this bot.

  Do not clean up TaskDimensions. There could be pending tasks and there's a
  possibility that a bot with the same ID could come up afterward (low chance in
  practice but it's a possibility). In this case, if TaskDimensions is deleted,
  the pending task would not be correctly run even when a bot comes back online
  as assert_bot_async() would fail to create the corresponding
  BotTaskDimensions.
  """
  bot_root_key = bot_management.get_root_key(bot_id)

  q = BotTaskDimensions.query(ancestor=bot_root_key).iter(keys_only=True)
  futures = ndb.delete_multi_async(q)
  futures.append(ndb.Key(BotDimensions, 1, parent=bot_root_key).delete_async())

  for f in futures:
    f.check_success()


def assert_task(request):
  """Makes sure the TaskRequest dimensions are listed as a known queue.

  This function must be called before storing the TaskRequest in the DB.

  When a cache miss occurs, a task queue is triggered.

  Warning: the task will not be run until the task queue ran, which causes a
  user visible delay. There is no SLA but expected range is normally seconds at
  worst. This only occurs on new kind of requests, which is not that often in
  practice.
  """
  assert not request.key, request.key
  dimensions_hash = hash_dimensions(request.properties.dimensions)
  task_dims_key = _get_task_dims_key(
      dimensions_hash, request.properties.dimensions)
  obj = task_dims_key.get()
  if obj:
    # Reduce the check to be 5~10 minutes earlier to help reduce an attack of
    # task queues when there's a strong on-going load of tasks happening. This
    # jitter is essentially removed from _ADVANCE window.
    jitter = datetime.timedelta(seconds=random.randint(5*60, 10*60))
    valid_until_ts = request.expiration_ts - jitter
    s = obj.match_request(request.properties.dimensions)
    if s:
      if s.valid_until_ts >= valid_until_ts:
        # Cache hit. It is important to reconfirm the dimensions because a hash
        # can be conflicting.
        logging.debug('assert_task(%d): hit', dimensions_hash)
        return
      else:
        logging.info(
            'assert_task(%d): set.valid_until_ts(%s) < expected(%s); '
            'triggering rebuild-task-cache',
            dimensions_hash, s.valid_until_ts, valid_until_ts)
    else:
      logging.info(
          'assert_task(%d): failed to match the dimensions; triggering '
          'rebuild-task-cache',
          dimensions_hash)
  else:
    logging.info(
        'assert_task(%d): new request kind; triggering rebuild-task-cache',
        dimensions_hash)

  data = {
    u'dimensions': request.properties.dimensions,
    u'dimensions_hash': str(dimensions_hash),
    u'valid_until_ts': request.expiration_ts + _ADVANCE,
  }
  payload = utils.encode_to_json(data)

  # If this task specifies an 'id' value, updates the cache inline since we know
  # there's only one bot that can run it, so it won't take long. This permits
  # tasks like 'terminate' tasks to execute faster.
  if request.properties.dimensions.get(u'id'):
    rebuild_task_cache(payload)
    return

  # We can't use the request ID since the request was not stored yet, so embed
  # all the necessary information.
  url = '/internal/taskqueue/rebuild-task-cache'
  if not utils.enqueue_task(
      url, queue_name='rebuild-task-cache', payload=payload):
    logging.error('Failed to enqueue TaskDimensions update %x', dimensions_hash)
    # Technically we'd want to raise a endpoints.InternalServerErrorException.
    # Raising anything that is not TypeError or ValueError is fine.
    raise Error('Failed to trigger task queue; please try again')


def get_queues(bot_id):
  """Queries all the known task queues in parallel and yields the task in order
  of priority.
  """
  assert isinstance(bot_id, unicode), repr(bot_id)
  data = memcache.get(bot_id, namespace='task_queues')
  if data is not None:
    logging.debug(
        'get_queues(%s): can run from %d queues (memcache)\n%s',
        bot_id, len(data), data)
    return data

  # Retrieve all the dimensions_hash that this bot could run that have
  # actually been triggered in the past. Since this is under a root entity, this
  # should be fast.
  now = utils.utcnow()
  bot_root_key = bot_management.get_root_key(bot_id)
  data = sorted(
      obj.key.integer_id() for obj in
      BotTaskDimensions.query(ancestor=bot_root_key)
      if obj.valid_until_ts >= now)
  memcache.set(bot_id, data, namespace='task_queues')
  logging.info(
      'get_queues(%s): Query in %.3fs: can run from %d queues\n%s',
      bot_id, (utils.utcnow()-now).total_seconds(), len(data), data)
  return data


def rebuild_task_cache(payload):
  """Rebuilds the TaskDimensions cache.

  This function is called in two cases:
  - A new kind of task request dimensions never seen before
  - The TaskDimensions.valid_until_ts expired

  It is a cache miss, query all the bots and check for the ones which can run
  the task.

  Warning: There's a race condition, where the TaskDimensions query could be
  missing some instances due to eventually coherent consistency in the BotInfo
  query. This only happens when there's new request dimensions set AND a bot
  that can run this task recently showed up.

  Runtime expectation: the scale on the number of bots that can run the task,
  via BotInfo.dimensions_flat filtering. As there can be tens of thousands of
  bots that can run the task, this can take a long time to store all the
  entities on a new kind of request. As such, it must be called in the backend.

  Arguments:
  - payload: dict as created in assert_task() with:
    - 'dimensions': dict of task dimensions to refresh
    - 'dimensions_hash': precalculated hash for dimensions
    - 'valid_until_ts': expiration_ts + _ADVANCE for how long this cache is
      valid

  Returns:
    True if everything was processed, False if it needs to be retried.
  """
  data = json.loads(payload)
  logging.debug('rebuild_task_cache(%s)', data)
  dimensions = data[u'dimensions']
  dimensions_hash = int(data[u'dimensions_hash'])
  valid_until_ts = utils.parse_datetime(data[u'valid_until_ts'])
  dimensions_flat = sorted(u'%s:%s' % (k, v) for k, v in dimensions.iteritems())

  now = utils.utcnow()
  updated = 0
  viable = 0
  try:
    pending = set()
    for bot_task_key in _yield_BotTaskDimensions_keys(
        dimensions_hash, dimensions_flat):
      viable += 1
      future = _refresh_BotTaskDimensions(
          bot_task_key, dimensions_flat, now, valid_until_ts)
      pending.add(future)
      updated += sum(1 for i in _cap_futures(pending) if i)
    updated += sum(1 for i in _flush_futures(pending) if i)

    # Done updating, now store the entity. Must use a transaction as there could
    # be other dimensions set in the entity.
    task_dims_key = _get_task_dims_key(dimensions_hash, dimensions)
    def run():
      obj = task_dims_key.get()
      if not obj:
        obj = TaskDimensions(key=task_dims_key)
      if obj.assert_request(now, valid_until_ts, dimensions_flat):
        obj.put()
      return obj

    try:
      datastore_utils.transaction(run)
    except datastore_utils.CommitError as e:
      # Still log an error but no need for a stack trace in the logs. It is
      # important to surface that the call failed so the task queue is retried
      # later.
      logging.error('Failed updating TaskDimensions: %s', e)
      return False
  finally:
    # Any of the _refresh_BotTaskDimensions() calls above could throw. Still log
    # how far we went.
    logging.debug(
        'rebuild_task_cache(%d) in %.3fs. viable bots: %d; bots updated: %d\n'
        '%s',
        dimensions_hash, (utils.utcnow()-now).total_seconds(), viable, updated,
        '\n'.join('  ' + d for d in dimensions_flat))
  return True


def tidy_stale():
  """Searches for all stale BotTaskDimensions and TaskDimensions and delete
  them.

  Their .valid_until_ts is compared to the current time and the entity is
  deleted if it's older.

  The number of entities processed is expected to be relatively low, in the few
  tens at most.
  """
  now = utils.utcnow()
  td = []
  btd = []

  _handle_task = lambda key: _remove_old_entity_async(key, now)

  @ndb.tasklet
  def _handle_bot_task(key):
    res = yield _remove_old_entity_async(key, now)
    if res:
      bot_id = key.parent().string_id()
      yield ndb.get_context().memcache_delete(bot_id, namespace='task_queues')
    raise ndb.Return(res)

  try:
    q = TaskDimensions.query().filter(TaskDimensions.valid_until_ts < now)
    td_future = q.map_async(_handle_task, batch_size=16, keys_only=True)

    q = BotTaskDimensions.query().filter(BotTaskDimensions.valid_until_ts < now)
    btd_future = q.map_async(_handle_bot_task, batch_size=16, keys_only=True)

    td = td_future.get_result()
    for k in td:
      if k:
        logging.info('- TD: %s', k.integer_id())
    btd = btd_future.get_result()
    for k in btd:
      if k:
        bot_id = k.parent().string_id()
        logging.debug('- BTD: %d for bot %s', k.integer_id(), bot_id)
  finally:
    logging.info(
        'tidy_stale() in %.3fs; TaskDimensions: found %d, deleted %d; '
        'BotTaskDimensions: found %d, deleted %d',
        (utils.utcnow() - now).total_seconds(),
        len(td), sum(1 for i in td if i), len(btd), sum(1 for i in btd if i))
