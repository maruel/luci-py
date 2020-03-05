# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Loading and interpretation of realms.cfg config files.

The primary purpose of the logic here is to keep datastore entities that are
part of AuthDB entity group up-to-date whenever external (realms.cfg) or
internal (permissions.DB) configs change.

refetch_config() is the actuator that makes sure that AuthDB entity group is
eventually fully up-to-date. It may do so through multiple separate commits if
necessary. Each commit produces a new AuthDB revision.
"""

import collections
import functools
import random
import time

from google.appengine.api import datastore_errors
from google.appengine.ext import ndb
from google.appengine.runtime import apiproxy_errors

from realms import permissions
from realms import validation

import replication


# Register the config validation hook.
validation.register()


# Information about fetched or previously processed realms.cfg.
#
# Comes either from LUCI Config (then `config_body` is set, but `db_rev` isn't)
# or from the datastore (then `db_rev` is set, but `config_body` isn't). All
# other fields are always set.
RealmsCfgRev = collections.namedtuple(
    'RealmsCfgRev',
    [
        'project_id',     # ID of the project in LUCI Config
        'config_rev',     # the revision the config was fetched from, FYI
        'config_digest',  # digest of the raw config body
        'config_body',    # byte blob with the fetched config (optional)
        'db_rev',         # revision of permissions DB revision used (optional)
    ])


# How many AuthDB revisions to produce when permission.DB changes (e.g. when
# a new permission is added to an existing role).
DB_REEVAL_REVISIONS = 10


class JobQueue(object):
  """A tiny abstraction for a list of callbacks that do AuthDB transactions.

  There should be no casual dependencies between jobs. Even through they will
  be executed sequentially, some may fail, and this does NOT stop processing of
  subsequent jobs.
  """

  def __init__(self):
    self.jobs = []

  def add(self, cb, *args):
    """Adds cb(*args) call to the queue."""
    self.jobs.append(functools.partial(cb, *args))

  def execute(self, txn_sleep_time):
    """Executes all enqueued jobs one by one, sleeping between them.

    This gives the datastore some time to "land" transactions. It's not a
    guarantee, but just a best effort attempt to avoid contention. If it
    happens, refetch_config() will resume unfinished work on the next iteration.

    Args:
      txn_sleep_time: how long to sleep between jobs.

    Returns:
      True if all tasks succeeded, False if at least one failed.
    """
    success = True
    for idx, job in enumerate(self.jobs):
      if idx:
        time.sleep(txn_sleep_time)
      try:
        job()
      except (
            apiproxy_errors.Error,
            datastore_errors.Error,
            replication.ReplicationTriggerError) as exc:
        logging.error(
            'Failed, will try again later: %s - %s',
            exc.__class__.__name__, exc)
        success = False
    return success


def refetch_config():
  """Called periodically in a cron job to import changes into the AuthDB.

  Returns:
    True on success, False on partial success or failure.
  """
  db = permissions.db()
  jobs = JobQueue()

  # If db.permissions has changed, we need to propagate changes into the AuthDB.
  check_permission_changes(db, jobs)

  # If either realms.cfg in one or more projects has changed, or the expansion
  # of roles into permissions has changed, we need to update flat expanded
  # realms representation in the AuthDB as well.
  latest = get_latest_revs_async()  # pylint: disable=assignment-from-no-return
  stored = get_stored_revs_async()  # pylint: disable=assignment-from-no-return
  check_config_changes(db, jobs, latest.get_result(), stored.get_result())

  # Land all scheduled transactions, sleeping between them for 2 sec. No rush.
  return jobs.execute(2.0)


def check_permission_changes(db, jobs):
  """Enqueues a job to update permissions list stored in the AuthDB.

  The AuthDB distributed to all services contains a list of all defined
  permissions. This list is a superset of permissions referenced by all realms.
  In particular, it may have entries that are not yet used in any realm.
  Downstream services are still interested in seeing them (for example, to
  compare with the list of permissions the service is interested in checking,
  to catch typos and misconfigurations).

  Args:
    db: a permissions.DB instance with current permissions and roles.
    jobs: a JobQueue instance to enqueue jobs to.
  """
  # TODO(vadimsh): Implement:
  #   1. Fetch the currently stored list of permissions.
  #   2. If same as db.permissions, exit.
  #   3. Transactionally:
  #      a. Fetch it again, compare to db.permissions.
  #      b. If different, update and trigger AuthDB replication.
  _ = db
  _ = jobs


def check_config_changes(db, jobs, latest, stored):
  """Enqueues jobs to update the AuthDB based on detected realms.cfg changes.

  Args:
    db: a permissions.DB instance with current permissions and roles.
    jobs: a JobQueue instance to enqueue jobs into.
    latest: a list of RealmsCfgRev with all fetched configs.
    stored: a list of RealmsCfgRev representing all currently applied configs.
  """
  latest_map = {r.project_id: r for r in latest}
  stored_map = {r.project_id: r for r in stored}

  assert len(latest_map) == len(latest)
  assert len(stored_map) == len(stored)

  # Shuffling helps to progress if one of the configs is somehow very
  # problematic (e.g. causes OOM). When the cron job is repeatedly retried, all
  # healthy configs will eventually be processed before the problematic ones.
  latest = latest[:]
  random.shuffle(latest)

  # List of RealmsCfgRev we'll need to reevaluate because they were generated
  # with stale db.revision.
  reeval = []

  # Detect changed realms.cfg and ones that need reevaluation.
  for rev in latest:
    cur = stored_map.get(rev.project_id)
    if not cur or cur.config_digest != rev.config_digest:
      jobs.add(update_realms, db, [rev])  # the realms.cfg body changed
    elif cur.db_rev != db.revision:
      reeval.append(rev)  # was evaluated with potentially stale roles

  # Detect realms.cfg that were removed completely.
  for rev in stored:
    if rev.project_id not in latest_map:
      jobs.add(delete_realms, rev.project_id)

  # Changing the permissions DB (e.g. adding a new permission to a widely used
  # role) may affect ALL projects. In this case generating a ton of AuthDB
  # revisions is wasteful. We could try to generate a single giant revision, but
  # it may end up being too big, hitting datastore limits. So we "heuristically"
  # split it into DB_REEVAL_REVISIONS revisions, hoping for the best.
  batch_size = max(1, len(reeval) // DB_REEVAL_REVISIONS)
  for i in range(0, len(reeval), batch_size):
    jobs.add(update_realms, db, reeval[i:i+batch_size])


@ndb.tasklet
def get_latest_revs_async():
  """Returns a list of all current RealmsCfgRev by querying LUCI Config."""
  # TODO(vadimsh): Implement via components.config API.
  raise ndb.Return([])


@ndb.tasklet
def get_stored_revs_async():
  """Returns a list of all stored RealmsCfgRev based on data in the AuthDB."""
  # TODO(vadimsh): Implement via a strongly consistent AuthDB datastore query.
  raise ndb.Return([])


def update_realms(db, revs):
  """Performs an AuthDB transaction that updates realms of some projects.

  It interprets realms.cfg, expanding them into an internal flat representation
  (using rules in `db`), and puts them into the AuthDB (if not already there).

  Args:
    db: a permissions.DB instance with current permissions and roles.
    revs: a list of RealmsCfgRev with fetched configs to reevaluate.
  """
  # TODO(vadimsh): Implement:
  #   1. Parse all text protos.
  #   2. Expand them into realms_pb2.Realms based on rules in `db`.
  #   3. In an AuthDB transaction visit all related ExpandedRealms entities and:
  #     a. If realms_pb2.Realms there is already up-to-date, just update
  #        associated config_rev, config_digest, db_rev (to avoid revisiting
  #        this config again).
  #     b. If realms_pb2.Realms is stale, update it (and all associated
  #        metadata). Remember this.
  #     c. If some realms_pb2.Realms were indeed updated, trigger AuthDB
  #        replication. Do NOT trigger it if we updated only bookkeeping
  #        metadata.
  _ = db
  _ = revs


def delete_realms(project_id):
  """Performs an AuthDB transaction that deletes all realms of some project.

  Args:
    project_id: ID of the project being deleted.
  """
  # TODO(vadimsh): Implement. Transactionally:
  #   1. Check ExpandedRealms(project_id) entity still exists.
  #   2. Delete it and trigger the replication if it does, noop if doesn't.
  _ = project_id
