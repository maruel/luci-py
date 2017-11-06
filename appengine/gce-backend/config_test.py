#!/usr/bin/python
# Copyright 2016 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Unit tests for config.py."""

import logging
import unittest

import test_env
test_env.setup_test_env()

from components import datastore_utils
from components import machine_provider
from components.config import validation
from test_support import test_case

import config
from proto import config_pb2


class UpdateConfigTest(test_case.TestCase):
  """Tests for config.update_template_configs."""

  def tearDown(self, *args, **kwargs):
    """Performs post-test case tear-down."""
    super(UpdateConfigTest, self).tearDown(*args, **kwargs)

    # Even though the datastore resets between test cases and
    # the underlying entity doesn't persist, the cache does.
    config.Configuration.clear_cache()

  def validator_test(self, validator, cfg, messages):
    ctx = validation.Context()
    validator(cfg, ctx)
    self.assertEquals(ctx.result().messages, [
      validation.Message(severity=logging.ERROR, text=m)
      for m in messages
    ])

  def install_mock(
      self,
      revision=None,
      template_config=None,
      manager_config=None,
      settings_config=None,
  ):
    """Installs a mock for config.config.get_self_config.

    Args:
      template_config: What to return when templates.cfg is requested. Defaults
        to an empty config_pb2.InstanceTemplateConfig instance.
      manager_config: What to return when managers.cfg is requested. Defaults
        to an empty config_pb2.InstanceGroupManagerConfig instance.
      settings_config: What to return when settings.cfg is requested. Defaults
        to an empty config_pb2.SettingsCfg instance.
    """
    def get_self_config(path, _,  **kwargs):
      self.assertIn(path, ('templates.cfg', 'managers.cfg', 'settings.cfg'))
      if path == 'templates.cfg':
        proto = template_config or config_pb2.InstanceTemplateConfig()
      elif path == 'managers.cfg':
        proto = manager_config or config_pb2.InstanceGroupManagerConfig()
      elif path == 'settings.cfg':
        proto = settings_config or config_pb2.SettingsCfg()
      return revision or 'mock-revision', proto
    self.mock(config.config, 'get_self_config', get_self_config)

  def test_empty_configs(self):
    """Ensures empty configs are successfully stored."""
    self.install_mock()

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_repeated_base_names(self):
    """Ensures duplicate base names reject the entire config."""
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-1',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-2',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-3',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-4',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-2',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-3',
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_too_many_instance_templates(self):
    template_config = config_pb2.InstanceTemplateConfig(
      templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-1',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-2',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-3',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-4',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-5',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-6',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-7',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-8',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-9',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-10',
            ),
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                base_name='base-name-11',
            ),
      ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_negative_guest_accelerator_count_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:-1'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_zero_guest_accelerator_count_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:0'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_empty_guest_accelerator_count_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_non_numeric_guest_accelerator_count_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:foo'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_guest_accelerator_count_too_high_rejected(self):
    """Ensures invalid host maintenance behavior is rejected."""
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:9999'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_valid_guest_accelerator_accepted(self):
    """Ensures invalid host maintenance behavior is rejected."""
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1:2'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failUnless(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_guest_accelerator_default_count_accepted(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=['accelerator-type-1'],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failUnless(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_multiple_guest_accelerator_accepted(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=[
                    'accelerator-type-1',
                    'accelerator-type-2:2',
                ],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failUnless(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_duplicate_guest_accelerator_types_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=[
                    'accelerator-type-1',
                    'accelerator-type-2:2',
                    'accelerator-type-1:3',
                ],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_too_many_guest_accelerator_types_rejected(self):
    template_config = config_pb2.InstanceTemplateConfig(
        templates=[
            config_pb2.InstanceTemplateConfig.InstanceTemplate(
                guest_accelerators=[
                    'accelerator-type-1',
                    'accelerator-type-2',
                    'accelerator-type-3',
                    'accelerator-type-4',
                    'accelerator-type-5',
                    'accelerator-type-6',
                    'accelerator-type-7',
                    'accelerator-type-8',
                    'accelerator-type-9',
                    'accelerator-type-10',
                    'accelerator-type-11',
                ],
            ),
        ],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_repeated_zone_different_base_name(self):
    """Ensures repeated zones in different base names are valid."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-1',
                zone='us-central1-a',
            ),
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-2',
                zone='us-central1-a',
            ),
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-3',
                zone='us-central1-a',
            ),
        ],
    )
    self.install_mock(manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failUnless(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_repeated_zone_same_base_name(self):
    """Ensures repeated zones in a base name reject the entire config."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-1',
                zone='us-central1-a',
            ),
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-2',
                zone='us-central1-b',
            ),
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                template_base_name='base-name-1',
                zone='us-central1-a',
            ),
        ],
    )
    self.install_mock(manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_minimum_size_exceeds_maximum_size(self):
    """Ensures repeated zones in a base name reject the entire config."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                maximum_size=1,
                minimum_size=2,
                template_base_name='base-name-1',
                zone='us-central1-a',
            ),
        ],
    )
    self.install_mock(manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_maximum_size_exceeds_maximum_allowed(self):
    """Ensures repeated zones in a base name reject the entire config."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[
            config_pb2.InstanceGroupManagerConfig.InstanceGroupManager(
                maximum_size=9999,
                template_base_name='base-name-1',
                zone='us-central1-a',
            ),
        ],
    )
    self.install_mock(manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.failIf(config.Configuration.cached().revision)

  def test_update_template_configs(self):
    """Ensures config is updated when revision changes."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[config_pb2.InstanceGroupManagerConfig.InstanceGroupManager()],
    )
    self.install_mock(revision='revision-1', manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failUnless(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'revision-1')

    template_config = config_pb2.InstanceTemplateConfig(
        templates=[config_pb2.InstanceTemplateConfig.InstanceTemplate()],
    )
    self.install_mock(revision='revision-2', template_config=template_config)

    config.update_template_configs()
    self.failUnless(config.Configuration.cached().template_config)
    self.failIf(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'revision-2')

  def test_update_template_configs_same_revision(self):
    """Ensures config is not updated when revision doesn't change."""
    manager_config = config_pb2.InstanceGroupManagerConfig(
        managers=[config_pb2.InstanceGroupManagerConfig.InstanceGroupManager()],
    )
    self.install_mock(manager_config=manager_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failUnless(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

    template_config = config_pb2.InstanceTemplateConfig(
        templates=[config_pb2.InstanceTemplateConfig.InstanceTemplate()],
    )
    self.install_mock(template_config=template_config)

    config.update_template_configs()
    self.failIf(config.Configuration.cached().template_config)
    self.failUnless(config.Configuration.cached().manager_config)
    self.assertEqual(config.Configuration.cached().revision, 'mock-revision')

  def test_settings_valid_mp_config(self):
    """Ensures base MP settings are correctly received if configured."""
    settings_config = config_pb2.SettingsCfg(mp_server='server')
    self.install_mock(settings_config=settings_config)

    self.assertEqual(config._get_settings()[1].mp_server, 'server')
    self.assertEqual(machine_provider.MachineProviderConfiguration.instance_url,
        'server')

  def test_settings_empty_mp_config(self):
    """Ensures base MP settings are correctly received if not configured."""
    settings_config = config_pb2.SettingsCfg()
    self.install_mock(settings_config=settings_config)

    mpdefault = machine_provider.MachineProviderConfiguration.get_instance_url()
    self.failIf(config._get_settings()[1].mp_server)
    self.assertEqual(machine_provider.MachineProviderConfiguration.instance_url,
        mpdefault)

  def test_validate_settings(self):
    self.validator_test(config.validate_settings_config,
        config_pb2.SettingsCfg(), [])
    self.validator_test(
        config.validate_settings_config,
        config_pb2.SettingsCfg(mp_server='http://url'),
        ['mp_server must start with "https://" or "http://localhost"'])
    self.validator_test(
        config.validate_settings_config,
        config_pb2.SettingsCfg(mp_server='url'),
        ['mp_server must start with "https://" or "http://localhost"'])


if __name__ == '__main__':
  unittest.main()
