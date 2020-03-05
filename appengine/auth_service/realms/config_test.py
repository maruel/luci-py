#!/usr/bin/env vpython
# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

# pylint: disable=no-value-for-parameter

import logging
import sys
import unittest

import test_env
test_env.setup_test_env()

import mock

from test_support import test_case

from realms import config
from realms import permissions


def fake_db(rev):
  return permissions.Builder(rev).finish()


def fake_realms_rev(project_id, config_digest, db_rev):
  return config.RealmsCfgRev(
      project_id, 'config-rev', config_digest, 'config-body', db_rev)


class CheckConfigChangesTest(test_case.TestCase):
  @mock.patch('realms.config.update_realms', autospec=True)
  @mock.patch('realms.config.delete_realms', autospec=True)
  def call(self, db, latest, stored, delete_realms_mock, update_realms_mock):
    updated = set()
    deleted = set()
    batches = []

    def do_update(_db, revs):
      batches.append(len(revs))
      for r in revs:
        self.assertNotIn(r.project_id, updated)
        self.assertNotIn(r.project_id, deleted)
        updated.add(r.project_id)
    update_realms_mock.side_effect = do_update

    def do_delete(project_id):
      self.assertNotIn(project_id, updated)
      self.assertNotIn(project_id, deleted)
      deleted.add(project_id)
    delete_realms_mock.side_effect = do_delete

    jobs = config.JobQueue()
    config.check_config_changes(db, jobs, latest, stored)
    self.assertTrue(jobs.execute(0.0))

    return updated, deleted, batches

  def test_noop_when_up_to_date(self):
    updated, deleted, _ = self.call(
        fake_db('db-rev'),
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest1', 'db-rev'),
        ],
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest1', 'db-rev'),
        ])
    self.assertEqual(updated, set())
    self.assertEqual(deleted, set())

  def test_new_projects(self):
    updated, deleted, _ = self.call(
        fake_db('db-rev'),
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest1', 'db-rev'),
        ],
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
        ])
    self.assertEqual(updated, {'proj2'})
    self.assertEqual(deleted, set())

  def test_updated_projects(self):
    updated, deleted, _ = self.call(
        fake_db('db-rev'),
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest1', 'db-rev'),
        ],
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest2', 'db-rev'),
        ])
    self.assertEqual(updated, {'proj2'})
    self.assertEqual(deleted, set())

  def test_deleted_projects(self):
    updated, deleted, _ = self.call(
        fake_db('db-rev'),
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
        ],
        [
            fake_realms_rev('proj1', 'digest1', 'db-rev'),
            fake_realms_rev('proj2', 'digest2', 'db-rev'),
        ])
    self.assertEqual(updated, set())
    self.assertEqual(deleted, {'proj2'})

  def test_db_revision_change(self):
    revs = [
        fake_realms_rev('proj%d' % i, 'digest1', 'db-rev1')
        for i in range(20)
    ]
    updated, deleted, batches = self.call(fake_db('db-rev2'), revs, revs)
    self.assertEqual(updated, {p.project_id for p in revs})  # all of them
    self.assertEqual(deleted, set())
    self.assertEqual(len(batches), config.DB_REEVAL_REVISIONS)


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.FATAL)
  unittest.main()
