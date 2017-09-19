# Copyright 2014 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Runs either task_runner.py, bot_main.py or bot_config.py.

The imports are done late so if an ImportError occurs, it is localized to this
command only.
"""

import code
import json
import logging
import os
import optparse
import shutil
import sys
import zipfile

import signal_trace

# That's from ../../../client/
from third_party.depot_tools import fix_encoding
from utils import logging_utils
from utils import zip_package

# This file can only be run as a zip.
THIS_FILE = os.path.abspath(zip_package.get_main_script_path())


# libusb1 expects to be directly in sys.path.
sys.path.insert(0, os.path.join(THIS_FILE, 'python_libusb1'))

# Copied from //client/utils/oauth.py.
sys.path.insert(0, os.path.join(THIS_FILE, 'third_party'))
sys.path.insert(0, os.path.join(THIS_FILE, 'third_party', 'pyasn1'))
sys.path.insert(0, os.path.join(THIS_FILE, 'third_party', 'pyasn1-modules'))
sys.path.insert(0, os.path.join(THIS_FILE, 'third_party', 'rsa'))

# The google library can occasionally get imported prior to the path
# maipulation above. If this happens, reload the module to pick up the version
# packaged in the bot_code in third_party.
path_to_zip = os.path.dirname(os.path.realpath(__file__))
path_to_google = os.path.join(path_to_zip, 'third_party', 'google')
import google
if google.__path__[0] != path_to_google:
  google = reload(google)

from bot_code import common


# TODO(maruel): Use depot_tools/subcommand.py. The goal here is to have all the
# sub commands packed into the single .zip file as a swiss army knife (think
# busybox but worse).


def CMDattributes(_args):
  """Prints out the bot's attributes."""
  from bot_code import bot_main
  botobj = bot_main.get_bot(bot_main.get_config())
  json.dump(
      bot_main.get_attributes(botobj), sys.stdout, indent=2,
      sort_keys=True, separators=(',', ': '))
  print('')
  return 0


def CMDconfig(_args):
  """Prints the config.json embedded in this zip."""
  logging_utils.prepare_logging(None)
  from bot_code import bot_main
  json.dump(bot_main.get_config(), sys.stdout, indent=2, sort_keys=True)
  print('')
  return 0


def CMDis_fine(_args):
  """Just reports that the code doesn't throw.

  That ensures that the bot has minimal viability before transfering control to
  it. For now, it just imports bot_main but later it'll check the config, etc.
  """
  # pylint: disable=unused-variable
  from bot_code import bot_main
  from config import bot_config
  # We're #goodenough.
  return 0


def CMDreboot(_args):
  """Utility subcommand that hides the difference between each OS to reboot
  the host."""
  logging_utils.prepare_logging(None)
  import os_utilities
  # This function doesn't return.
  os_utilities.host_reboot()
  # Should never reach here.
  return 1


def CMDrun_isolated(args):
  """Internal command to run an isolated command."""
  sys.path.insert(0, os.path.join(THIS_FILE, 'client'))
  # run_isolated setups logging by itself.
  import run_isolated
  return run_isolated.main(args)


def CMDsetup(_args):
  """Setup the bot to auto-start but doesn't start the bot."""
  logging_utils.prepare_logging(os.path.join('logs', 'bot_config.log'))
  from bot_code import bot_main
  bot_main.setup_bot(True)
  return 0


def CMDserver(_args):
  """Prints the server url. It's like 'config' but easier to parse."""
  logging_utils.prepare_logging(None)
  from bot_code import bot_main
  print bot_main.get_config()['server']
  return 0


def CMDshell(args):
  """Starts a shell with api.* in.."""
  logging_utils.prepare_logging(None)
  logging_utils.set_console_level(logging.DEBUG)

  from bot_code import bot_main
  from api import os_utilities
  from api import platforms
  local_vars = {
    'bot_main': bot_main,
    'json': json,
    'os_utilities': os_utilities,
    'platforms': platforms,
  }
  # Can't use: from api.platforms import *
  local_vars.update(
      (k, v) for k, v in platforms.__dict__.iteritems()
      if not k.startswith('_'))

  if args:
    for arg in args:
      exec code.compile_command(arg) in local_vars
  else:
    code.interact(
        'Locals:\n  ' + '\n  '.join( sorted(local_vars)), None, local_vars)
  return 0


def CMDstart_bot(args):
  """Starts the swarming bot."""
  logging_utils.prepare_logging(os.path.join('logs', 'swarming_bot.log'))
  from bot_code import bot_main
  logging.info(
      'importing bot_main: %s, %s', THIS_FILE, bot_main.generate_version())
  adb_logger = logging.getLogger('adb')
  logging_utils.prepare_logging(os.path.join('logs', 'adb.log'),
                                adb_logger)
  adb_logger.setLevel(logging.DEBUG)
  for child in ('high', 'low', 'usb', 'cmd'):
    adb_logger.getChild(child).setLevel(logging.DEBUG)
  adb_logger.propagate = False
  result = bot_main.main(args)
  logging.info('bot_main exit code: %d', result)
  return result


def CMDstart_slave(args):
  """Ill named command that actually sets up the bot then start it."""
  # TODO(maruel): Rename function.
  logging_utils.prepare_logging(os.path.join('logs', 'bot_config.log'))

  parser = optparse.OptionParser()
  parser.add_option(
      '--survive', action='store_true',
      help='Do not reboot the host even if bot_config.setup_bot() asked to')
  options, args = parser.parse_args(args)

  try:
    from bot_code import bot_main
    bot_main.setup_bot(options.survive)
  except Exception:
    logging.exception('bot_main.py failed.')

  logging.info('Starting the bot: %s', THIS_FILE)
  return common.exec_python([THIS_FILE, 'start_bot'])


def CMDtask_runner(args):
  """Internal command to run a swarming task."""
  logging_utils.prepare_logging(os.path.join('logs', 'task_runner.log'))
  from bot_code import task_runner
  return task_runner.main(args)


def CMDversion(_args):
  """Prints the version of this file and the hash of the code."""
  logging_utils.prepare_logging(None)
  print zip_package.generate_version()
  return 0


def main():
  if os.getenv('CHROME_REMOTE_DESKTOP_SESSION') == '1':
    # Disable itself when run under Google Chrome Remote Desktop, as it's
    # normally started at the console and starting up via Remote Desktop would
    # cause multiple bots to run concurrently on the host.
    print >> sys.stderr, (
        'Inhibiting Swarming bot under Google Chrome Remote Desktop.')
    return 0

  # Always make the current working directory the directory containing this
  # file. It simplifies assumptions.
  os.chdir(os.path.dirname(THIS_FILE))
  # Always create the logs dir first thing, before printing anything out.
  if not os.path.isdir('logs'):
    os.mkdir('logs')

  # This is necessary so os.path.join() works with unicode path. No kidding.
  # This must be done here as each of the command take wildly different code
  # path and this must be run in every case, as it causes really unexpected
  # issues otherwise, especially in module os.path.
  fix_encoding.fix_encoding()

  # This is extremely useful to debug hangs.
  signal_trace.register()

  if os.path.basename(THIS_FILE) == 'swarming_bot.zip':
    # Self-replicate itself right away as swarming_bot.1.zip and restart the bot
    # process as this copy. This enables LKGBC logic.
    print >> sys.stderr, 'Self replicating pid:%d.' % os.getpid()
    if os.path.isfile('swarming_bot.1.zip'):
      os.remove('swarming_bot.1.zip')
    shutil.copyfile('swarming_bot.zip', 'swarming_bot.1.zip')
    cmd = ['swarming_bot.1.zip'] + sys.argv[1:]
    print >> sys.stderr, 'cmd: %s' % cmd
    return common.exec_python(cmd)

  # sys.argv[0] is the zip file itself.
  cmd = 'start_slave'
  args = []
  if len(sys.argv) > 1:
    cmd = sys.argv[1]
    args = sys.argv[2:]

  fn = getattr(sys.modules[__name__], 'CMD%s' % cmd, None)
  if fn:
    try:
      return fn(args)
    except ImportError:
      logging.exception('Failed to run %s', cmd)
      with zipfile.ZipFile(THIS_FILE, 'r') as f:
        logging.error('Files in %s:\n%s', THIS_FILE, f.namelist())
      return 1

  print >> sys.stderr, 'Unknown command %s' % cmd
  return 1


if __name__ == '__main__':
  sys.exit(main())
