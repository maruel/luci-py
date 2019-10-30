#!/usr/bin/env vpython
# Copyright 2019 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import argparse
import logging
import os
import sys
import threading
import traceback
import unittest

import six
from nose2 import discover

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LUCI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(THIS_DIR)))
PLUGINS_DIR = os.path.join(THIS_DIR, 'nose2_plugins')
CLIENT_THIRD_PARTY_DIR = os.path.join(LUCI_DIR, 'client', 'third_party')


def show_all_stacktraces():
  """This is used to show where the threads are stucked."""
  frames = sys._current_frames()
  for th in threading.enumerate():
    print('Thread:%s' % th.name)
    if th.ident is None:
      print('not started, skipped')
      continue
    traceback.print_stack(frames[th.ident], limit=None)

  # exit(1) only exits this thread.
  os._exit(1)


def run_tests(python3=False):
  """Discover unittests and run them using nose2"""
  hook_args(sys.argv)

  plugins = []
  if python3:
    plugins.append('py3filter')

  # fix_encoding
  sys.path.insert(0, CLIENT_THIRD_PARTY_DIR)
  from depot_tools import fix_encoding
  fix_encoding.fix_encoding()

  # add nose2 plugin dir to path
  sys.path.insert(0, PLUGINS_DIR)

  if sys.platform == 'darwin':
    # TODO(crbug.com/1019105): remove this.
    timer = threading.Timer(30, show_all_stacktraces)
    timer.start()

  discover(plugins=plugins)

  if sys.platform == 'darwin':
    timer.cancel()


def hook_args(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('--log-level')
  args, _ = parser.parse_known_args(argv)

  if args.verbose:
    unittest.TestCase.maxDiff = None

  if not args.log_level:
    # override default log level
    logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
  run_tests(python3=six.PY3)
