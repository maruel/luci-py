#!/usr/bin/env vpython

# Copyright 2019 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import os
import sys
import logging

import six
from nose2 import discover

SWARMING_DIR = os.path.dirname(os.path.abspath(__file__))
APPENGINE_DIR = os.path.dirname(SWARMING_DIR)
LUCI_DIR = os.path.dirname(os.path.dirname(SWARMING_DIR))
CLIENT_THIRDPARTY_DIR = os.path.join(LUCI_DIR, 'client', 'third_party')
PLUGINS_DIR = os.path.join(APPENGINE_DIR,
                           'components', 'test_support', 'nose2_plugins')


def main():
  # TODO(jwata) delete this adhoc path insertion
  # after fixing swarming_test_env.setup_test_env
  if six.PY2:
    import swarming_test_env
    swarming_test_env.setup_test_env()
  if six.PY3:
    sys.path.insert(0, CLIENT_THIRDPARTY_DIR)

  from depot_tools import fix_encoding
  fix_encoding.fix_encoding()

  # add nose2 plugin dir to path
  sys.path.insert(0, PLUGINS_DIR)

  discover()


def _has_arg(argv, arg):
  return any([arg in a for a in argv])


if __name__ == '__main__':
  if not _has_arg(sys.argv, '--log-level'):
    logging.basicConfig(level=logging.CRITICAL)
  main()
