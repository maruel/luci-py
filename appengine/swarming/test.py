#!/usr/bin/env vpython
# Copyright 2019 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import os
import sys

import six

SWARMING_DIR = os.path.dirname(os.path.abspath(__file__))
SWARMING_BOT_DIR = os.path.join(SWARMING_DIR, 'swarming_bot')
APPENGINE_DIR = os.path.dirname(SWARMING_DIR)
COMPONENTS_DIR = os.path.join(APPENGINE_DIR, 'components')

def main():
  # import dir that has test_support
  sys.path.insert(0, COMPONENTS_DIR)

  # TODO(jwata): delete this adhoc path insertion
  # after fixing swarming_test_env.setup_test_env
  if six.PY2:
    import swarming_test_env
    swarming_test_env.setup_test_env()

  sys.path.insert(0, SWARMING_BOT_DIR)
  import test_env_bot
  test_env_bot.setup_test_env()

  # execute test runner
  from test_support import parallel_test_runner
  return parallel_test_runner.run_tests(python3=six.PY3)


if __name__ == '__main__':
  main()
