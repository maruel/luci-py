#!/usr/bin/python
# Copyright 2016 The LUCI Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""Unit tests for instance_group_managers.py."""

import unittest

import test_env
test_env.setup_test_env()

from google.appengine.ext import ndb

from components import datastore_utils
from components import net
from test_support import test_case

import models
import instance_group_managers


class CreateTest(test_case.TestCase):
  """Tests for instance_group_managers.create."""

  def test_entity_doesnt_exist(self):
    """Ensures nothing happens when the entity doesn't exist."""
    key = ndb.Key(models.InstanceGroupManager, 'fake-key')

    instance_group_managers.create(key)

    self.failIf(key.get())

  def test_parent_nonexistent(self):
    """Ensures nothing happens when parent does not exist."""
    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
    ).put()

    instance_group_managers.create(key)
    self.failIf(key.get().url)

  def test_parent_project_unspecified(self):
    """Ensures nothing happens when parent does not specify project."""
    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
    ).put()
    models.InstanceTemplateRevision(key=key.parent(), url='url').put()

    instance_group_managers.create(key)
    self.failIf(key.get().url)

  def test_parent_url_unspecified(self):
    """Ensures nothing happens when parent does not specify URL."""
    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
    ).put()
    models.InstanceTemplateRevision(key=key.parent(), project='project').put()

    instance_group_managers.create(key)
    self.failIf(key.get().url)

  def test_creates(self):
    """Ensures an instance group manager is created."""
    def create_instance_group_manager(*args, **kwargs):
      return {'targetLink': 'url'}
    self.mock(
        instance_group_managers.gce.Project,
        'create_instance_group_manager',
        create_instance_group_manager,
    )

    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
        minimum_size=2,
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        project='project',
        url='instance-template-url',
    ).put()
    expected_url = 'url'

    instance_group_managers.create(key)
    self.assertEqual(key.get().url, expected_url)

  def test_updates_when_already_created(self):
    """Ensures an instance group manager is updated when already created."""
    def create_instance_group_manager(*args, **kwargs):
      raise net.Error('', 409, '')
    def get_instance_group_manager(*args, **kwargs):
      return {'selfLink': 'url'}
    self.mock(
        instance_group_managers.gce.Project,
        'create_instance_group_manager',
        create_instance_group_manager,
    )
    self.mock(
        instance_group_managers.gce.Project,
        'get_instance_group_manager',
        get_instance_group_manager,
    )

    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
        minimum_size=2,
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        project='project',
        url='instance-template-url',
    ).put()
    expected_url = 'url'

    instance_group_managers.create(key)
    self.assertEqual(key.get().url, expected_url)

  def test_doesnt_update_when_creation_fails(self):
    """Ensures an instance group manager is not updated when creation fails."""
    def create_instance_group_manager(*args, **kwargs):
      raise net.Error('', 400, '')
    self.mock(
        instance_group_managers.gce.Project,
        'create_instance_group_manager',
        create_instance_group_manager,
    )

    key = models.InstanceGroupManager(
        key=instance_group_managers.get_instance_group_manager_key(
            'base-name',
            'revision',
            'zone',
        ),
        minimum_size=2,
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        project='project',
        url='instance-template-url',
    ).put()

    self.assertRaises(net.Error, instance_group_managers.create, key)
    self.failIf(key.get().url)


class ScheduleCreationTest(test_case.TestCase):
  """Tests for instance_group_managers.schedule_creation."""

  def setUp(self, *args, **kwargs):
    def enqueue_task(*args, **kwargs):
      self.failUnless(kwargs.get('params', {}).get('key'))
      entity = ndb.Key(urlsafe=kwargs['params']['key']).get()
      entity.url = kwargs['params']['key']
      entity.put()
      return True

    super(ScheduleCreationTest, self).setUp(*args, **kwargs)
    self.mock(instance_group_managers.utils, 'enqueue_task', enqueue_task)

  def test_enqueues_task(self):
    """Ensures a task is enqueued."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        active=[
            key,
        ],
        url='url',
    ).put()
    models.InstanceGroupManager(key=key).put()
    expected_url = key.urlsafe()

    instance_group_managers.schedule_creation()

    self.assertEqual(key.get().url, expected_url)

  def test_instance_template_revision_inactive(self):
    """Ensures no task is enqueued for inactive instance template revisions."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        active=[
            key,
        ],
        url='url',
    ).put()
    models.InstanceGroupManager(key=key).put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_template_revision_missing(self):
    """Ensures no task is enqueued for missing instance template revisions."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceGroupManager(key=key).put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_template_revision_no_url(self):
    """Ensures no task is enqueued when instance template URL is missing."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        active=[
            key,
        ],
    ).put()
    models.InstanceGroupManager(key=key).put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_group_manager_inactive(self):
    """Ensures no task is enqueued for inactive instance group managers."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        url='url',
    ).put()
    models.InstanceGroupManager(key=key).put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_group_manager_drained(self):
    """Ensures no task is enqueued for drained instance group managers."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        drained=[
            key,
        ],
        url='url',
    ).put()
    models.InstanceGroupManager(key=key).put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_group_manager_missing(self):
    """Ensures no task is enqueued for missing instance group managers."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        active=[
            key,
        ],
        url='url',
    ).put()
    key = models.InstanceGroupManager().put()

    instance_group_managers.schedule_creation()

    self.failIf(key.get().url)

  def test_instance_group_manager_already_created(self):
    """Ensures no task is enqueued for existing instance group managers."""
    key = instance_group_managers.get_instance_group_manager_key(
        'base-name', 'revision', 'zone')
    models.InstanceTemplate(
        key=key.parent().parent(),
        active=key.parent(),
    ).put()
    models.InstanceTemplateRevision(
        key=key.parent(),
        active=[
            key,
        ],
        url='instance-template-url',
    ).put()
    models.InstanceGroupManager(key=key, url='url').put()
    expected_url = 'url'

    instance_group_managers.schedule_creation()

    self.assertEqual(key.get().url, expected_url)


if __name__ == '__main__':
  unittest.main()
