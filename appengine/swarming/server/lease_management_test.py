#!/usr/bin/python
# Copyright 2015 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Unit tests for lease_management.py."""

import datetime
import json
import logging
import sys
import unittest

import test_env
test_env.setup_test_env()

from google.appengine.ext import ndb
from protorpc.remote import protojson
import webtest

from components import machine_provider
from components import utils
from test_support import test_case

import bot_management
import lease_management
from proto import bots_pb2


def rpc_to_json(rpc_message):
  """Converts the given RPC message to a POSTable JSON dict.

  Args:
    rpc_message: A protorpc.message.Message instance.

  Returns:
    A string representing a JSON dict.
  """
  return json.loads(protojson.encode_message(rpc_message))


class CheckForConnectionTest(test_case.TestCase):
  """Tests for lease_management.check_for_connection."""

  def test_not_connected(self):
    machine_lease = lease_management.MachineLease(
        bot_id='bot-id',
        client_request_id='req-id',
        hostname='bot-id',
        instruction_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'mt'),
    )
    machine_lease.put()
    bot_management.bot_event(
        event_type='bot_leased',
        bot_id=machine_lease.hostname,
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )

    lease_management.check_for_connection(machine_lease)
    self.failUnless(bot_management.get_info_key(machine_lease.bot_id).get())
    self.failUnless(machine_lease.key.get().client_request_id)
    self.failIf(machine_lease.key.get().connection_ts)

  def test_connected(self):
    machine_lease = lease_management.MachineLease(
        bot_id='bot-id',
        client_request_id='req-id',
        hostname='bot-id',
        instruction_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'mt'),
    )
    machine_lease.put()
    bot_management.bot_event(
        event_type='bot_leased',
        bot_id=machine_lease.hostname,
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )
    bot_management.bot_event(
        event_type='bot_connected',
        bot_id=machine_lease.hostname,
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )

    lease_management.check_for_connection(machine_lease)
    self.failUnless(bot_management.get_info_key(machine_lease.bot_id).get())
    self.failUnless(machine_lease.key.get().client_request_id)
    self.failUnless(machine_lease.key.get().connection_ts)

  def test_connected_earlier_than_instructed(self):
    bot_management.bot_event(
        event_type='bot_connected',
        bot_id='bot-id',
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )
    machine_lease = lease_management.MachineLease(
        bot_id='bot-id',
        client_request_id='req-id',
        hostname='bot-id',
        instruction_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'mt'),
    )
    machine_lease.put()
    bot_management.bot_event(
        event_type='bot_leased',
        bot_id=machine_lease.hostname,
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )

    lease_management.check_for_connection(machine_lease)
    self.failUnless(bot_management.get_info_key(machine_lease.bot_id).get())
    self.failUnless(machine_lease.key.get().client_request_id)
    self.failIf(machine_lease.key.get().connection_ts)

  def test_missing(self):
    self.mock(lease_management, 'release', lambda *args, **kwargs: True)

    machine_lease = lease_management.MachineLease(
        bot_id='bot-id',
        client_request_id='req-id',
        hostname='bot-id',
        instruction_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'mt'),
    )
    machine_lease.put()

    lease_management.check_for_connection(machine_lease)
    self.failIf(bot_management.get_info_key(machine_lease.bot_id).get())
    self.failIf(machine_lease.key.get().client_request_id)
    self.failIf(machine_lease.key.get().connection_ts)

  def test_dead(self):
    def is_dead(_self, _now):
      return True
    self.mock(bot_management.BotInfo, 'is_dead', is_dead)
    self.mock(lease_management, 'release', lambda *args, **kwargs: True)

    machine_lease = lease_management.MachineLease(
        bot_id='bot-id',
        client_request_id='req-id',
        hostname='bot-id',
        instruction_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'mt'),
    )
    machine_lease.put()
    bot_management.bot_event(
        event_type='bot_leased',
        bot_id=machine_lease.hostname,
        external_ip=None,
        authenticated_as=None,
        dimensions=None,
        state=None,
        version=None,
        quarantined=False,
        task_id='',
        task_name=None,
    )

    lease_management.check_for_connection(machine_lease)
    self.failIf(bot_management.get_info_key(machine_lease.bot_id).get())
    self.failIf(machine_lease.key.get().client_request_id)
    self.failIf(machine_lease.key.get().connection_ts)


class ComputeUtilizationTest(test_case.TestCase):
  """Tests for lease_management.compute_utilization."""
  APP_DIR = test_env.APP_DIR

  def test_no_machine_provider_bots(self):
    bots = [
    ]
    def fetch_page(*_args, **_kwargs):
      return bots, None
    self.mock(lease_management.datastore_utils, 'fetch_page', fetch_page)

    lease_management.MachineType(
        id='machine-type',
        target_size=1,
    ).put()
    key = ndb.Key(lease_management.MachineTypeUtilization, 'machine-type')

    lease_management.compute_utilization()

    self.failIf(key.get())

  def test_machine_provider_bots(self):
    ndb.get_context().set_cache_policy(lambda _: None)
    now = utils.utcnow()
    bots = [
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot1'),
            machine_type='machine-type-1',
            last_seen_ts=now,
        ),
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot2'),
            machine_type='machine-type-1',
            last_seen_ts=now,
        ),
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot3'),
            machine_type='machine-type-2',
            last_seen_ts=now,
            task_id='task',
        ),
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot4'),
            machine_type='machine-type-3',
            last_seen_ts=now,
            task_id='task',
        ),
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot5'),
            machine_type='machine-type-3',
            last_seen_ts=now,
        ),
        bot_management.BotInfo(
            key=bot_management.get_info_key('bot6'),
            machine_type='machine-type-3',
            last_seen_ts=now,
            task_id='task',
        ),
    ]
    ndb.put_multi(bots)

    obj1 = lease_management.MachineType(id='machine-type-1', target_size=2)
    obj1.put()
    obj2 = lease_management.MachineType(id='machine-type-2', target_size=1)
    obj2.put()
    obj3 = lease_management.MachineType(id='machine-type-3', target_size=1)
    obj3.put()

    lease_management.compute_utilization()

    u1 = ndb.Key(lease_management.MachineTypeUtilization,
        obj1.key.string_id()).get()
    self.assertEqual(u1.busy, 0)
    self.assertEqual(u1.idle, 2)
    self.failUnless(u1.last_updated_ts)

    u2 = ndb.Key(lease_management.MachineTypeUtilization,
        obj2.key.string_id()).get()
    self.assertEqual(u2.busy, 1)
    self.assertEqual(u2.idle, 0)
    self.failUnless(u2.last_updated_ts)

    u3 = ndb.Key(lease_management.MachineTypeUtilization,
        obj3.key.string_id()).get()
    self.assertEqual(u3.busy, 2)
    self.assertEqual(u3.idle, 1)
    self.failUnless(u3.last_updated_ts)


class DrainExcessTest(test_case.TestCase):
  """Tests for lease_management.drain_excess."""

  def test_no_machine_types(self):
    lease_management.drain_excess()

    self.failIf(lease_management.MachineLease.query().count())

  def test_nothing_to_drain(self):
    key = lease_management.MachineType(
        target_size=1,
    ).put()
    key = lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()

    lease_management.drain_excess()

    self.assertEqual(lease_management.MachineLease.query().count(), 1)
    self.failIf(key.get().drained)

  def test_drain_one(self):
    key = lease_management.MachineType(
        target_size=0,
    ).put()
    key = lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()

    lease_management.drain_excess()

    self.assertEqual(lease_management.MachineLease.query().count(), 1)
    self.assertTrue(key.get().drained)

  def test_drain_all(self):
    key = lease_management.MachineType(
        enabled=False,
        target_size=3,
    ).put()
    lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()
    lease_management.MachineLease(
        id='%s-1' % key.id(),
        machine_type=key,
    ).put()
    lease_management.MachineLease(
        id='%s-2' % key.id(),
        machine_type=key,
    ).put()

    lease_management.drain_excess()

    self.assertEqual(lease_management.MachineLease.query().count(), 3)
    for machine_lease in lease_management.MachineLease.query():
      self.assertTrue(machine_lease.drained)

  def test_drain_batched(self):
    key = lease_management.MachineType(
        enabled=False,
        target_size=2,
    ).put()
    lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()
    lease_management.MachineLease(
        id='%s-1' % key.id(),
        machine_type=key,
    ).put()
    key = lease_management.MachineType(
        enabled=False,
        target_size=2,
    ).put()
    lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()
    lease_management.MachineLease(
        id='%s-1' % key.id(),
        machine_type=key,
    ).put()
    key = lease_management.MachineType(
        target_size=0,
    ).put()
    lease_management.MachineLease(
        id='%s-0' % key.id(),
        machine_type=key,
    ).put()

    # Choice of 2, 2, 1 above and 3 here ensures at least one batch contains
    # MachineLease entities created for two different MachineTypes.
    lease_management.drain_excess(max_concurrent=3)

    self.assertEqual(lease_management.MachineLease.query().count(), 5)
    for machine_lease in lease_management.MachineLease.query():
      self.assertTrue(machine_lease.drained)


class EnsureBotInfoExistsTest(test_case.TestCase):
  """Tests for lease_management.ensure_bot_info_exists."""

  def test_creates(self):
    key = lease_management.MachineLease(
        hostname='hostname',
        lease_id='lease-id',
        lease_expiration_ts=utils.utcnow(),
        machine_type=ndb.Key(lease_management.MachineType, 'machine-type'),
    ).put()

    lease_management.ensure_bot_info_exists(key.get())

    machine_lease = key.get()
    bot_info = bot_management.get_info_key(machine_lease.bot_id).get()
    self.assertEqual(machine_lease.bot_id, machine_lease.hostname)
    self.assertEqual(bot_info.lease_id, machine_lease.lease_id)
    self.assertEqual(
        bot_info.lease_expiration_ts, machine_lease.lease_expiration_ts)
    self.assertEqual(bot_info.machine_type, machine_lease.machine_type.id())


class EnsureEntitiesExistTest(test_case.TestCase):
  """Tests for lease_management.ensure_entities_exist."""

  def test_no_machine_types(self):
    lease_management.ensure_entities_exist()

    self.failIf(lease_management.MachineLease.query().count())

  def test_no_enabled_machine_types(self):
    lease_management.MachineType(
        enabled=False,
        target_size=3,
    ).put()

    lease_management.ensure_entities_exist()

    self.failIf(lease_management.MachineLease.query().count())

  def test_one_enabled_machine_type(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )

    key = lease_management.MachineType(
        id='machine-type',
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(key.get().early_release_secs, 0)
    self.assertEqual(key.get().lease_duration_secs, 1)
    self.assertEqual(key.get().target_size, 1)
    self.assertEqual(lease_management.MachineLease.query().count(), 1)

  def test_two_enabled_machine_types(self):
    def fetch_machine_types():
      return {
          'machine-type-a': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type-a',
              target_size=1,
          ),
          'machine-type-b': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type-b',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )

    lease_management.MachineType(
        id='machine-type-a',
        target_size=1,
    ).put()
    lease_management.MachineType(
        id='machine-type-b',
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(lease_management.MachineLease.query().count(), 2)
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-a-0'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-b-0'))

  def test_one_machine_type_multiple_batches(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=5,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )

    lease_management.MachineType(
        id='machine-type',
        target_size=5,
    ).put()

    # Choice of 3 here and 5 above ensures MachineLeases are created in two
    # batches of differing sizes.
    lease_management.ensure_entities_exist(max_concurrent=3)

    self.assertEqual(lease_management.MachineLease.query().count(), 5)
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-0'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-1'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-2'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-3'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-4'))

  def test_three_machine_types_multiple_batches(self):
    def fetch_machine_types():
      return {
          'machine-type-a': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type-a',
              target_size=2,
          ),
          'machine-type-b': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type-b',
              target_size=2,
          ),
          'machine-type-c': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type-c',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )

    lease_management.MachineType(
        id='machine-type-a',
        target_size=2,
    ).put()
    lease_management.MachineType(
        id='machine-type-b',
        target_size=2,
    ).put()
    lease_management.MachineType(
        id='machine-type-c',
        target_size=1,
    ).put()

    # Choice of 2, 2, 1 above and 3 here ensures at least one batch contains
    # MachineLease entities created for two different MachineTypes.
    lease_management.ensure_entities_exist(max_concurrent=3)

    self.assertEqual(lease_management.MachineLease.query().count(), 5)
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-a-0'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-a-1'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-b-0'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-b-1'))
    self.failUnless(lease_management.MachineLease.get_by_id('machine-type-c-0'))

  def test_enable_machine_type(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        enabled=False,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.failUnless(key.get().enabled)

  def test_update_machine_type(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=2,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        enabled=True,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(key.get().lease_duration_secs, 2)

  def test_enable_and_update_machine_type(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=2,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        enabled=False,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.failUnless(key.get().enabled)
    self.assertEqual(key.get().lease_duration_secs, 2)

  def test_disable_machine_type(self):
    def fetch_machine_types():
      return {
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        enabled=True,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.failIf(key.get().enabled)

  def test_machine_lease_exists_mismatched_not_updated(self):
    key = lease_management.MachineType(
        early_release_secs=0,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()
    key = lease_management.MachineLease(
        id='%s-0' % key.id(),
        early_release_secs=1,
        lease_duration_secs=2,
        machine_type=key,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=200,
        ),
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(lease_management.MachineLease.query().count(), 1)
    self.assertEqual(key.get().early_release_secs, 1)
    self.assertEqual(key.get().lease_duration_secs, 2)
    self.assertEqual(key.get().mp_dimensions.disk_gb, 200)

  def test_machine_lease_exists_mismatched_updated(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )

    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()
    key = lease_management.MachineLease(
        id='%s-0' % key.id(),
        early_release_secs=1,
        lease_duration_secs=2,
        lease_expiration_ts=utils.utcnow(),
        machine_type=key,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=200,
        ),
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(lease_management.MachineLease.query().count(), 1)
    self.assertEqual(key.get().early_release_secs, 0)
    self.assertEqual(key.get().lease_duration_secs, 1)
    self.assertEqual(key.get().mp_dimensions.disk_gb, 100)

  def test_daily_schedule_resize(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
              schedule=bots_pb2.Schedule(
                  daily=[bots_pb2.DailySchedule(
                      start='0:00',
                      end='1:00',
                      days_of_the_week=xrange(7),
                      target_size=3,
                  )],
              ),
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    self.mock(
        lease_management.utils,
        'utcnow',
        lambda: datetime.datetime(1969, 1, 1, 0, 30),
    )

    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(lease_management.MachineLease.query().count(), 3)
    self.assertEqual(key.get().target_size, 3)

  def test_daily_schedule_resize_to_default(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
              schedule=bots_pb2.Schedule(
                  daily=[bots_pb2.DailySchedule(
                      start='0:00',
                      end='1:00',
                      days_of_the_week=xrange(7),
                      target_size=3,
                  )],
              ),
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    self.mock(
        lease_management.utils,
        'utcnow',
        lambda: datetime.datetime(1969, 1, 1, 2),
    )

    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.assertEqual(lease_management.MachineLease.query().count(), 1)
    self.assertEqual(key.get().target_size, 1)

  def test_daily_schedule_resize_to_zero(self):
    def fetch_machine_types():
      return {
          'machine-type': bots_pb2.MachineType(
              early_release_secs=0,
              lease_duration_secs=1,
              mp_dimensions=['disk_gb:100'],
              name='machine-type',
              target_size=1,
              schedule=bots_pb2.Schedule(
                  daily=[bots_pb2.DailySchedule(
                      start='0:00',
                      end='1:00',
                      days_of_the_week=xrange(7),
                      target_size=0,
                  )],
              ),
          ),
      }
    self.mock(
        lease_management.bot_groups_config,
        'fetch_machine_types',
        fetch_machine_types,
    )
    self.mock(
        lease_management.utils,
        'utcnow',
        lambda: datetime.datetime(1969, 1, 1, 0, 30),
    )

    key = lease_management.MachineType(
        id='machine-type',
        early_release_secs=0,
        lease_duration_secs=1,
        mp_dimensions=machine_provider.Dimensions(
            disk_gb=100,
        ),
        target_size=1,
    ).put()

    lease_management.ensure_entities_exist()

    self.failIf(lease_management.MachineLease.query().count())
    self.failIf(key.get().target_size)


class GetTargetSize(test_case.TestCase):
  """Tests for lease_management.get_target_size."""

  def test_no_schedules(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule())

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 2), 2)

  def test_wrong_day(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        daily=[bots_pb2.DailySchedule(
            start='1:00',
            end='2:00',
            days_of_the_week=xrange(5),
            target_size=3,
        )],
    ))
    now = datetime.datetime(2012, 1, 1, 1, 2)

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 2, now), 2)

  def test_right_day(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        daily=[bots_pb2.DailySchedule(
            start='1:00',
            end='2:00',
            days_of_the_week=xrange(7),
            target_size=3,
        )],
    ))
    now = datetime.datetime(2012, 1, 1, 1, 2)

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 2, now), 3)

  def test_no_utilization(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        load_based=[bots_pb2.LoadBased(
            maximum_size=5,
            minimum_size=3,
        )],
    ))

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 4), 4)

  def test_utilization(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        load_based=[bots_pb2.LoadBased(
            maximum_size=6,
            minimum_size=2,
        )],
    ))
    lease_management.MachineTypeUtilization(
        id='mt',
        busy=4,
        idle=0,
    ).put()

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 3), 6)

  def test_load_based_fallback(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        daily=[bots_pb2.DailySchedule(
            start='1:00',
            end='2:00',
            days_of_the_week=xrange(5),
            target_size=3,
        )],
        load_based=[bots_pb2.LoadBased(
            maximum_size=6,
            minimum_size=2,
        )],
    ))
    lease_management.MachineTypeUtilization(
        id='mt',
        busy=4,
        idle=0,
    ).put()
    now = datetime.datetime(2012, 1, 1, 1, 2)

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 3, now), 6)

  def test_upper_bound(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        load_based=[bots_pb2.LoadBased(
            maximum_size=4,
            minimum_size=2,
        )],
    ))
    lease_management.MachineTypeUtilization(
        id='mt',
        busy=4,
        idle=0,
    ).put()

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 3), 4)

  def test_drop_dampening(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        load_based=[bots_pb2.LoadBased(
            maximum_size=100,
            minimum_size=1,
        )],
    ))
    lease_management.MachineTypeUtilization(
        id='mt',
        busy=60,
        idle=20,
    ).put()

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 100, 50), 99)

  def test_lower_bound(self):
    config = bots_pb2.MachineType(schedule=bots_pb2.Schedule(
        load_based=[bots_pb2.LoadBased(
            maximum_size=4,
            minimum_size=2,
        )],
    ))
    lease_management.MachineTypeUtilization(
        id='mt',
        busy=0,
        idle=4,
    ).put()

    self.assertEqual(
        lease_management.get_target_size(config.schedule, 'mt', 1, 3), 2)


if __name__ == '__main__':
  logging.basicConfig(
      level=logging.DEBUG if '-v' in sys.argv else logging.ERROR)
  unittest.main()
