# Copyright 2013 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""Swarming bot main process.

This is the program that communicates with the Swarming server, ensures the code
is always up to date and executes a child process to run tasks and upload
results back.

It manages self-update and rebooting the host in case of problems.
"""

import json
import logging
import optparse
import os
import subprocess
import sys
import time
import zipfile

# pylint: disable-msg=W0403
import bot
import logging_utils
import os_utilities
import xsrf_client
from utils import net
from utils import on_error
from utils import zip_package


# Path to this file or the zip containing this file.
THIS_FILE = os.path.abspath(zip_package.get_main_script_path())

# Root directory containing this file or the zip containing this file.
ROOT_DIR = os.path.dirname(THIS_FILE)


# See task_runner.py for documentation.
TASK_FAILED = 89


def get_attributes():
  """Returns bot_config.py's get_attributes() dict."""
  # Importing this administrator provided script could have side-effects on
  # startup. That is why it is imported late.
  import bot_config
  return bot_config.get_attributes()


def get_attributes_failsafe():
  """Returns fail-safe default attributes."""
  try:
    hostname = os_utilities.get_hostname_short()
  except Exception as e:
    hostname = str(e)
  try:
    ip = os_utilities.get_ip()
  except Exception as e:
    ip = str(e)

  return {
    'dimensions': {},
    'id': hostname,
    'ip': ip,
  }


def get_current_state(started_ts, sleep_streak):
  """Returns dict with a state of the bot reported to the server with each poll.

  Supposed to be use only for dynamic state that changes while bot is running.
  Use 'attributes' for static state that doesn't change over time.

  The server can not use this state for immediate scheduling purposes (use
  'dimensions' for that), but it can use it for maintenance and bookkeeping
  tasks.

  Args:
    started_ts: when bot started polling, seconds since epoch by a local clock.
    sleep_streak: number of consecutive sleeps up till now.
  """
  # TODO(vadimsh): Send also results of 'uptime' command? Maybe also current
  # open file descriptors, processes or any other leaky resources. So that the
  # server can decided to reboot the bot to clean up.
  return {
    'disk': os_utilities.get_free_disk(),
    'ram': os_utilities.get_physical_ram(),
    'running_time': time.time() - started_ts,
    'sleep_streak': sleep_streak,
    'started_ts': started_ts,
  }


def on_after_task(botobj, failure, internal_failure):
  """Hook function called after a task."""
  try:
    import bot_config
    return bot_config.on_after_task(botobj, failure, internal_failure)
  except Exception as e:
    logging.exception('Failed to call hook on_after_task(): %s', e)


def post_error_task(remote, attributes, error, task_id):
  """Posts given error as failure cause for the task.

  This is used in case of internal code error, and this causes the task to
  become BOT_DIED.

  Arguments:
    remote: An XrsfRemote instance.
    attributes: This bot's attributes.
    error: String representing the problem.
    task_id: Task that had an internal error. When the Swarming server sends
        commands to a bot, even though they could be completely wrong, the
        server assumes the job as running. Thus this function acts as the
        exception handler for incoming commands from the Swarming server. If for
        any reason the local test runner script can not be run successfully,
        this function is invoked.
  """
  # TODO(maruel): It could be good to send a signal when the task hadn't started
  # at all. In this case the server could retry the task even if it doesn't have
  # 'idempotent' set. See
  # https://code.google.com/p/swarming/issues/detail?id=108.
  logging.error('Error: %s\n%s', attributes, error)
  data = {
    'id': attributes.get('id'),
    'message': error,
    'task_id': task_id,
  }
  return remote.url_read_json(
      '/swarming/api/v1/bot/task_error/%s' % task_id, data=data)


def run_bot(remote, error):
  """Runs the bot until it reboots or self-update."""
  # TODO(maruel): This should be part of the 'health check' and the bot
  # shouldn't allow itself to upgrade in this condition.
  # https://code.google.com/p/swarming/issues/detail?id=112
  # Catch all exceptions here so the bot doesn't die on startup, which is
  # annoying to recover. In that case, we set a special property to catch these
  # and help the admin fix the swarming_bot code more quickly.
  attributes = {}
  try:
    # If zip_package.generate_version() fails, we still want the server to do
    # the /server_ping before calculating the attributes.
    attributes['version'] = zip_package.generate_version()
  except Exception as e:
    error = str(e)

  try:
    # First thing is to get an arbitrary url. This also ensures the network is
    # up and running, which is necessary before trying to get the FQDN below.
    remote.url_read('/server_ping')
  except Exception as e:
    # url_read() already traps pretty much every exceptions. This except clause
    # is kept there "just in case".
    error = str(e)

  try:
    # The fully qualified domain name will uniquely identify this machine to the
    # server, so we can use it to give a deterministic id for this bot. Also
    # store as lower case, since it is already case-insensitive.
    attributes.update(get_attributes())
  except Exception as e:
    attributes.update(get_attributes_failsafe())
    error = str(e)

  logging.info('Attributes: %s', attributes)

  # Handshake to get an XSRF token even if there were errors.
  remote.xsrf_request_params = {'attributes': attributes.copy()}
  remote.refresh_token()

  botobj = bot.Bot(remote, attributes)
  if error:
    botobj.post_error('Startup failure: %s' % error)

  started_ts = time.time()
  consecutive_sleeps = 0
  while True:
    try:
      state = get_current_state(started_ts, consecutive_sleeps)
      did_something = poll_server(botobj, remote, attributes, state)
      if did_something:
        consecutive_sleeps = 0
      else:
        consecutive_sleeps += 1
    except Exception as e:
      botobj.post_error(str(e))
      consecutive_sleeps = 0


def poll_server(botobj, remote, attributes, state):
  """Polls the server to run one loop.

  Returns True if executed some action, False if server asked the bot to sleep.
  """
  data = {
    'attributes': attributes,
    'state': state,
  }
  resp = remote.url_read_json('/swarming/api/v1/bot/poll', data=data)
  logging.debug('Server response:\n%s', resp)

  cmd = resp['cmd']
  if cmd == 'sleep':
    time.sleep(resp['duration'])
    return False

  if cmd == 'run':
    run_manifest(botobj, remote, attributes, resp['manifest'])
  elif cmd == 'update':
    update_bot(botobj, remote, resp['version'])
  elif cmd == 'restart':
    botobj.restart(resp['message'])
  else:
    raise ValueError('Unexpected command: %s\n%s' % (cmd, resp))

  return True


def run_manifest(botobj, remote, attributes, manifest):
  """Defers to task_runner.py."""
  # Ensure the manifest is valid. This can throw a json decoding error. Also
  # raise if it is empty.
  if not manifest:
    raise ValueError('Empty manifest')

  # Necessary to signal an internal_failure. This occurs when task_runner fails
  # to execute the command. It is important to note that this data is extracted
  # before any I/O is done, like writting the manifest to disk.
  task_id = manifest['task_id']

  failure = False
  internal_failure = False
  msg = None
  try:
    # We currently do not clean up the 'work' directory now is it compartmented.
    # TODO(maruel): Compartmentation should be done via tag. It is important to
    # not be too aggressive about deletion because running a task with a warm
    # cache has important performance benefit.
    # https://code.google.com/p/swarming/issues/detail?id=149
    if not os.path.isdir('work'):
      os.makedirs('work')

    path = os.path.join('work', 'test_run.json')
    with open(path, 'wb') as f:
      f.write(json.dumps(manifest))
    # TODO(maruel): Rename local_test_runner to task_runner or something
    # relevant.
    command = [
      sys.executable, THIS_FILE, 'local_test_runner',
      '-S', remote.url,
      '-f', path,
    ]
    logging.debug('Running command: %s', command)
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT_DIR)
    out = proc.communicate()[0]

    failure = proc.returncode == TASK_FAILED
    internal_failure = not failure and bool(proc.returncode)
    if internal_failure:
      msg = 'Execution failed, internal error:\n%s' % out
  except Exception as e:
    # Failures include IOError when writing if the disk is full, OSError if
    # swarming_bot.zip doesn't exist anymore, etc.
    msg = 'Internal exception occured: %s' % str(e)
    internal_failure = True
  finally:
    if internal_failure:
      post_error_task(remote, attributes, msg, task_id)
    on_after_task(botobj, failure, internal_failure)


def update_bot(botobj, remote, version):
  """Downloads the new version of the bot code and then runs it.

  Use alternating files; first load swarming_bot.1.zip, then swarming_bot.2.zip,
  never touching swarming_bot.zip which was the originally bootstrapped file.

  Does not return.

  TODO(maruel): Create LKGBC:
  https://code.google.com/p/swarming/issues/detail?id=112
  """
  # Alternate between .1.zip and .2.zip.
  new_zip = 'swarming_bot.1.zip'
  if os.path.basename(THIS_FILE) == new_zip:
    new_zip = 'swarming_bot.2.zip'

  # Download as a new file.
  url = remote.url + '/get_slave_code/%s' % version
  if not net.url_retrieve(new_zip, url):
    raise Exception('Unable to download %s from %s.' % (new_zip, url))

  logging.info('Restarting to %s.', new_zip)
  sys.stdout.flush()
  sys.stderr.flush()

  cmd = [sys.executable, new_zip, 'start_slave', '--survive']
  if sys.platform in ('cygwin', 'win32'):
    # (Tentative) It is expected that subprocess.Popen() behaves a tad better
    # on Windows than os.exec*(), which has to be emulated since there's no OS
    # provided implementation. This means processes will accumulate as the bot
    # is restarted, which could be a problem long term.
    sys.exit(subprocess.call(cmd))
  else:
    # On OSX, launchd will be unhappy if we quit so the old code bot process
    # has to outlive the new code child process. Launchd really wants the main
    # process to survive, and it'll restart it if it disappears. os.exec*()
    # replaces the process so this is fine.
    os.execv(sys.executable, cmd)

  # This code runs only if bot failed to respawn itself.
  botobj.post_error(remote, 'Bot failed to respawn after update')




def get_config():
  """Returns the data from config.json.

  First try the config.json inside the zip. If not present or not running inside
  swarming_bot.zip, use the one beside the file.
  """
  if THIS_FILE.endswith('.zip'):
    with zipfile.ZipFile(THIS_FILE, 'r') as f:
      return json.load(f.open('config.json'))

  with open(os.path.join(ROOT_DIR, 'config.json'), 'r') as f:
    return json.load(f)


def main(args):
  # Add SWARMING_HEADLESS into environ so subcommands know that they are running
  # in a headless (non-interactive) mode.
  os.environ['SWARMING_HEADLESS'] = '1'

  # TODO(maruel): Get rid of all flags and support no option at all.
  # https://code.google.com/p/swarming/issues/detail?id=111
  parser = optparse.OptionParser(
      usage='%prog [options]',
      description=sys.modules[__name__].__doc__)
  # TODO(maruel): Always True.
  parser.add_option('-v', '--verbose', action='count', default=0,
                    help='Set logging level to INFO, twice for DEBUG.')

  config = get_config()
  server = config['server']
  on_error.report_on_exception_exit(server)
  error = None
  try:
    # Do this late so an error is reported. It could happen when a flag is
    # removed but the auto-update script was not upgraded properly.
    options, args = parser.parse_args(args)
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging_utils.set_console_level(levels[min(options.verbose, len(levels)-1)])
    if args:
      parser.error('Unsupported args.')
  except Exception as e:
    # Do not reboot here, because it would just cause a reboot loop.
    error = str(e)
  remote = xsrf_client.XsrfRemote(server, '/swarming/api/v1/bot/handshake')
  return run_bot(remote, error)
