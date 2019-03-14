# Copyright 2012 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""This module defines Isolate Server backend url handlers."""

import binascii
import logging
import time
import zlib

import webapp2
from google.appengine import runtime
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.ext import ndb

import config
import gcs
import mapreduce_jobs
import model
import stats
import template
from components import decorators
from components import utils


### Utility


class Accumulator(object):
  """Accumulates output from a generator."""
  def __init__(self, source):
    self.accumulated = []
    self._source = source

  def __iter__(self):
    for i in self._source:
      self.accumulated.append(i)
      yield i
      del i


def _split_payload(request, chunk_size, max_chunks):
  """Splits a binary payload into elements of |chunk_size| length.

  Returns each chunks.
  """
  content = request.request.body
  if len(content) % chunk_size:
    msg = (
        'Payload must be in increments of %d bytes, had %d bytes total, last '
        'chunk was of length %d' % (
              chunk_size,
              len(content),
              len(content) % chunk_size))
    logging.error(msg)
    request.abort(400, detail=msg)

  count = len(content) / chunk_size
  if count > max_chunks:
    msg = (
        'Requested more than %d hash digests in a single request, '
        'aborting' % count)
    logging.warning(msg)
    request.abort(400, detail=msg)

  return [content[i * chunk_size: (i + 1) * chunk_size] for i in xrange(count)]


def _payload_to_hashes(request, namespace):
  """Converts a raw payload into hashes as bytes."""
  h = model.get_hash(namespace)
  return _split_payload(request, h.digest_size, model.MAX_KEYS_PER_DB_OPS)


def _throttle_futures(futures, limit):
  finished = []
  if len(futures) <= limit:
    return futures, finished
  while len(futures) > limit:
    ndb.Future.wait_any(futures)
    tmp = []
    for f in futures:
      if f.done():
        f.get_result()
        finished.append(f)
      else:
        tmp.append(f)
    futures = tmp
  return futures, finished


def _incremental_delete(query, delete_async):
  """Applies |delete| to objects in a query asynchrously.

  This function is itself synchronous.

  Arguments:
  - query: iterator of items to process.
  - delete_async: callback that accepts an object to delete and returns a
        ndb.Future.

  Returns the number of objects found.
  """
  count = 0
  deleted_count = 0
  futures = []
  for item in query:
    count += 1
    if not (count % 1000):
      logging.debug('Found %d items', count)
    futures.append(delete_async(item))
    deleted_count += 1

    # Throttle.
    futures, _ = _throttle_futures(futures, 100)

  for f in futures:
    f.get_result()
  return deleted_count


def _yield_orphan_gcs_files(gs_bucket):
  """Iterate over the whole GCS bucket for unreferenced files.

  Yields:
    filepath in the bucket
  """
  futures = {}
  cutoff = time.time() - 60*60
  for filepath, filestats in gcs.list_files(gs_bucket):
    # If the file was uploaded in the last hour, ignore it.
    if filestats.st_ctime >= cutoff:
      continue

    # This must match the logic in model.get_entry_key(). Since this request
    # will in practice touch every item, do not use memcache since it'll
    # mess it up by loading every items in it.
    # TODO(maruel): Batch requests to use get_multi_async() similar to
    # datastore_utils.page_queries().
    future = model.entry_key_from_id(filepath).get_async(
        use_cache=False, use_memcache=False)
    futures[future] = filepath

    if len(futures) > 20:
      future = ndb.Future.wait_any(futures)
      filepath = futures.pop(future)
      if future.get_result():
        continue
      yield filepath
  while futures:
    future = ndb.Future.wait_any(futures)
    filepath = futures.pop(future)
    if future.get_result():
      continue
    yield filepath



### Restricted handlers


class InternalCleanupOldEntriesWorkerHandler(webapp2.RequestHandler):
  """Removes the old data from the datastore.

  Only a task queue task can use this handler.
  """
  # pylint: disable=R0201
  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      runtime.DeadlineExceededError)
  @decorators.require_taskqueue('cleanup')
  def post(self):
    q = model.ContentEntry.query(
        model.ContentEntry.expiration_ts < utils.utcnow()
        ).iter(keys_only=True)
    total = _incremental_delete(q, model.delete_entry_and_gs_entry)
    logging.info('Deleting %s expired entries', total)


class InternalObliterateWorkerHandler(webapp2.RequestHandler):
  """Deletes all the stuff."""
  # pylint: disable=R0201
  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      runtime.DeadlineExceededError)
  @decorators.require_taskqueue('cleanup')
  def post(self):
    logging.info('Deleting ContentEntry')
    _incremental_delete(
        model.ContentEntry.query().iter(keys_only=True),
        lambda k: k.delete_async())

    gs_bucket = config.settings().gs_bucket
    logging.info('Deleting GS bucket %s', gs_bucket)
    _incremental_delete(
        (i[0] for i in gcs.list_files(gs_bucket)),
        lambda filenames: gcs.delete_file_async(gs_bucket, filenames))

    logging.info('Flushing memcache')
    # High priority (.isolated files) are cached explicitly. Make sure ghosts
    # are zapped too.
    memcache.flush_all()
    logging.info('Finally done!')


def _find_orphan_gcs_files(gs_bucket):
  """Iterate over the whole GCS bucket for unreferenced files.

  Yields:
    filepath in the bucket
  """
  futures = {}
  cutoff = time.time() - 60*60
  for filepath, filestats in gcs.list_files(gs_bucket):
    # If the file was uploaded in the last hour, ignore it.
    if filestats.st_ctime >= cutoff:
      continue

    # This must match the logic in model.get_entry_key(). Since this request
    # will touch every ContentEntry, do not use memcache since it'll
    # overflow it up by loading every items in it.
    future = model.entry_key_from_id(filepath).get_async(use_memcache=False)
    futures[future] = filepath

    if len(futures) > 100:
      ndb.Future.wait_any(futures)
      tmp = {}
      for f, p in futures.iteritems():
        if f.done():
          f.get_result()
          yield p
          continue
        tmp[f] = p
      futures = tmp

  while futures:
    ndb.Future.wait_any(futures)
    tmp = {}
    for f, p in futures.iteritems():
      if f.done():
        f.get_result()
        yield p
        continue
      tmp[f] = p
    futures = tmp

class InternalCleanupTrimLostWorkerHandler(webapp2.RequestHandler):
  """Removes the GS files that are not referenced anymore.

  It can happen for example when a ContentEntry is deleted without the file
  properly deleted.

  Only a task queue task can use this handler.
  """
  # pylint: disable=R0201
  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      runtime.DeadlineExceededError)
  @decorators.require_taskqueue('cleanup')
  def post(self):
    """Enumerates all GS files and delete those that do not have an associated
    ContentEntry.
    """
    gs_bucket = config.settings().gs_bucket
    total = _incremental_delete(
        _find_orphan_gcs_files(gs_bucket),
        lambda f: gcs.delete_file_async(gs_bucket, f))
    logging.info('Deleted %d lost GS files', total)

    # TODO(maruel): Find all the empty directories that are old and remove them.
    # We need to safe guard against the race condition where a user would upload
    # to this directory.


class InternalCleanupTriggerHandler(webapp2.RequestHandler):
  """Triggers a taskqueue to clean up."""
  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      runtime.DeadlineExceededError)
  @decorators.require_cronjob
  def get(self, name):
    if name in ('obliterate', 'old', 'orphaned', 'trim_lost'):
      url = '/internal/taskqueue/cleanup/' + name
      # The push task queue name must be unique over a ~7 days period so use
      # the date at second precision, there's no point in triggering each of
      # time more than once a second anyway.
      now = utils.utcnow().strftime('%Y-%m-%d_%I-%M-%S')
      if utils.enqueue_task(url, 'cleanup', name=name + '_' + now):
        self.response.out.write('Triggered %s' % url)
      else:
        self.abort(500, 'Failed to enqueue a cleanup task, see logs')
    else:
      self.abort(404, 'Unknown job')


class InternalTagWorkerHandler(webapp2.RequestHandler):
  """Tags hot ContentEntry entities that were tested for presence.

  Updates .expiration_ts and .next_tag_ts in ContentEntry to note that a client
  tagged them.

  This makes sure they are not evicted from the LRU cache too fast.
  """
  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      runtime.DeadlineExceededError)
  @decorators.require_taskqueue('tag')
  def post(self, namespace, timestamp):
    saved = 0
    digests = []
    now = utils.timestamp_to_datetime(long(timestamp))
    expiration = config.settings().default_expiration
    try:
      digests = _payload_to_hashes(self, namespace)
      # Requests all the entities at once.
      fetch_futures = ndb.get_multi_async(
          model.get_entry_key(namespace, binascii.hexlify(d)) for d in digests)

      save_futures = []
      while fetch_futures:
        # Return opportunistically the first entity that can be retrieved.
        fetch_futures, done = _throttle_futures(
            fetch_futures, len(fetch_futures)-1)
        for f in done:
          item = f.get_result()
          if item and item.next_tag_ts < now:
            # Update the timestamp. Add a bit of pseudo randomness.
            item.expiration_ts, item.next_tag_ts = model.expiration_jitter(
                now, expiration)
            save_futures.append(item.put_async())
            saved += 1
        save_futures, _ = _throttle_futures(save_futures, 100)

      for f in save_futures:
        f.get_result()
      logging.info(
          'Timestamped %d entries out of %d', saved, len(digests))
    except Exception as e:
      logging.error('Failed to stamp entries: %s\n%d entries', e, len(digests))
      raise


class InternalVerifyWorkerHandler(webapp2.RequestHandler):
  """Verify the SHA-1 matches for an object stored in Cloud Storage."""

  @staticmethod
  def purge_entry(entry, message, *args):
    """Logs error message, deletes |entry| from datastore and GS."""
    logging.error(
        'Verification failed for %s: %s', entry.key.id(), message % args)
    model.delete_entry_and_gs_entry_async(entry.key).get_result()

  @decorators.silence(
      datastore_errors.InternalError,
      datastore_errors.Timeout,
      datastore_errors.TransactionFailedError,
      gcs.TransientError,
      runtime.DeadlineExceededError)
  @decorators.require_taskqueue('verify')
  def post(self, namespace, hash_key):
    original_request = self.request.get('req')
    entry = model.get_entry_key(namespace, hash_key).get()
    if not entry:
      logging.error('Failed to find entity\n%s', original_request)
      return
    if entry.is_verified:
      logging.warning('Was already verified\n%s', original_request)
      return
    if entry.content is not None:
      logging.error(
          'Should not be called with inline content\n%s', original_request)
      return

    # Get GS file size.
    gs_bucket = config.settings().gs_bucket
    gs_file_info = gcs.get_file_info(gs_bucket, entry.key.id())

    # It's None if file is missing.
    if not gs_file_info:
      # According to the docs, GS is read-after-write consistent, so a file is
      # missing only if it wasn't stored at all or it was deleted, in any case
      # it's not a valid ContentEntry.
      self.purge_entry(entry, 'No such GS file\n%s', original_request)
      return

    # Expected stored length and actual length should match.
    if gs_file_info.size != entry.compressed_size:
      self.purge_entry(entry,
          'Bad GS file: expected size is %d, actual size is %d\n%s',
          entry.compressed_size, gs_file_info.size,
          original_request)
      return

    save_to_memcache = (
        entry.compressed_size <= model.MAX_MEMCACHE_ISOLATED and
        entry.is_isolated)
    expanded_size = 0
    digest = model.get_hash(namespace)
    data = None

    try:
      # Start a loop where it reads the data in block.
      stream = gcs.read_file(gs_bucket, entry.key.id())
      if save_to_memcache:
        # Wraps stream with a generator that accumulates the data.
        stream = Accumulator(stream)

      for data in model.expand_content(namespace, stream):
        expanded_size += len(data)
        digest.update(data)
        # Make sure the data is GC'ed.
        del data

      # Hashes should match.
      if digest.hexdigest() != hash_key:
        self.purge_entry(entry,
            'SHA-1 do not match data\n'
            '%d bytes, %d bytes expanded, expected %d bytes\n%s',
            entry.compressed_size, expanded_size,
            entry.expanded_size, original_request)
        return

    except gcs.NotFoundError as e:
      # Somebody deleted a file between get_file_info and read_file calls.
      self.purge_entry(
          entry, 'File was unexpectedly deleted\n%s', original_request)
      return
    except (gcs.ForbiddenError, gcs.AuthorizationError) as e:
      # Misconfiguration in Google Storage ACLs. Don't delete an entry, it may
      # be fine. Maybe ACL problems would be fixed before the next retry.
      logging.warning(
          'CloudStorage auth issues (%s): %s', e.__class__.__name__, e)
      # Abort so the job is retried automatically.
      return self.abort(500)
    except (gcs.FatalError, zlib.error, IOError) as e:
      # ForbiddenError and AuthorizationError inherit FatalError, so this except
      # block should be last.
      # It's broken or unreadable.
      self.purge_entry(entry,
          'Failed to read the file (%s): %s\n%s',
          e.__class__.__name__, e, original_request)
      return

    # Verified. Data matches the hash.
    entry.expanded_size = expanded_size
    entry.is_verified = True
    future = entry.put_async()
    logging.info(
        '%d bytes (%d bytes expanded) verified\n%s',
        entry.compressed_size, expanded_size, original_request)
    if save_to_memcache:
      model.save_in_memcache(namespace, hash_key, ''.join(stream.accumulated))
    future.wait()
    return


class InternalStatsUpdateHandler(webapp2.RequestHandler):
  """Called every few minutes to update statistics."""
  @decorators.require_cronjob
  def get(self):
    minutes = stats.cron_generate_stats()
    if minutes is not None:
      logging.info('Processed %d minutes', minutes)


class InternalStatsSendToBQHandler(webapp2.RequestHandler):
  """Called every few minutes to update statistics."""
  @decorators.require_cronjob
  def get(self):
    stats.cron_send_to_bq()


### Mapreduce related handlers


class InternalLaunchMapReduceJobWorkerHandler(webapp2.RequestHandler):
  """Called via task queue or cron to start a map reduce job."""
  @decorators.require_taskqueue(mapreduce_jobs.MAPREDUCE_TASK_QUEUE)
  def post(self, job_id):  # pylint: disable=R0201
    mapreduce_jobs.launch_job(job_id)


###


def get_routes():
  """Returns the routes to be executed on the backend."""
  # Namespace can be letters, numbers, '-', '.' and '_'.
  namespace = r'/<namespace:%s>' % model.NAMESPACE_RE
  # Do not enforce a length limit to support different hashing algorithm. This
  # should represent a valid hex value.
  hashkey = r'/<hash_key:[a-f0-9]{4,}>'
  # This means a complete key is required.
  namespace_key = namespace + hashkey

  return [
    # Triggers a taskqueue.
    webapp2.Route(
        r'/internal/cron/cleanup/trigger/<name:[a-z_]+>',
        InternalCleanupTriggerHandler),

    # Cleanup tasks.
    webapp2.Route(
        r'/internal/taskqueue/cleanup/old',
        InternalCleanupOldEntriesWorkerHandler),
    webapp2.Route(
        r'/internal/taskqueue/cleanup/obliterate',
        InternalObliterateWorkerHandler),
    webapp2.Route(
        r'/internal/taskqueue/cleanup/trim_lost',
        InternalCleanupTrimLostWorkerHandler),

    # Tasks triggered by other request handlers.
    webapp2.Route(
        r'/internal/taskqueue/tag%s/<timestamp:\d+>' % namespace,
        InternalTagWorkerHandler),
    webapp2.Route(
        r'/internal/taskqueue/verify%s' % namespace_key,
        InternalVerifyWorkerHandler),

    # Stats
    webapp2.Route(
        r'/internal/cron/stats/update', InternalStatsUpdateHandler),
    webapp2.Route(
        r'/internal/cron/stats/send_to_bq', InternalStatsSendToBQHandler),

    # Mapreduce related urls.
    webapp2.Route(
        r'/internal/taskqueue/mapreduce/launch/<job_id:[^\/]+>',
        InternalLaunchMapReduceJobWorkerHandler),
  ]


def create_application(debug):
  """Creates the url router for the backend.

  The backend only implements urls under /internal/.
  """
  # Necessary due to email sent by cron job.
  template.bootstrap()
  return webapp2.WSGIApplication(get_routes(), debug=debug)
