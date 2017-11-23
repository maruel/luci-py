# Copyright 2013 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Runs a Swarming task.

Downloads all the necessary files to run the task, executes the command and
streams results back to the Swarming server.

The process exit code is 0 when the task was executed, even if the task itself
failed. If there's any failure in the setup or teardown, like invalid packet
response, failure to contact the server, etc, a non zero exit code is used. It's
up to the calling process (bot_main.py) to signal that there was an internal
failure and to cancel this task run and ask the server to retry it.
"""

import json
import logging
import optparse
import os
import signal
import sys
import time
import traceback

from utils import file_path
from utils import net
from utils import on_error
from utils import subprocess42
from utils import zip_package

from libs import luci_context

import bot_auth
import remote_client


# Path to this file or the zip containing this file.
THIS_FILE = os.path.abspath(zip_package.get_main_script_path())


# Sends a maximum of 100kb of stdout per task_update packet.
MAX_CHUNK_SIZE = 102400


# Maximum wait between task_update packet when there's no output.
MAX_PACKET_INTERVAL = 30


# Minimum wait between task_update packet when there's output.
MIN_PACKET_INTERNAL = 10


# Current task_runner_out version.
OUT_VERSION = 3


# On Windows, SIGTERM is actually sent as SIGBREAK since there's no real
# SIGTERM.  SIGBREAK is not defined on posix since it's a pure Windows concept.
SIG_BREAK_OR_TERM = (
    signal.SIGBREAK if sys.platform == 'win32' else signal.SIGTERM)


# Used to implement monotonic_time for a clock that never goes backward.
_last_now = 0


def monotonic_time():
  """Returns monotonically increasing time."""
  global _last_now
  now = time.time()
  if now > _last_now:
    # TODO(maruel): If delta is large, probably worth alerting via ereporter2.
    _last_now = now
  return _last_now


def get_run_isolated():
  """Returns the path to itself to run run_isolated.

  Mocked in test to point to the real run_isolated.py script.
  """
  return [sys.executable, THIS_FILE, 'run_isolated']


def get_isolated_args(work_dir, task_details, isolated_result,
                      bot_file, run_isolated_flags):
  """Returns the command to call run_isolated. Mocked in tests."""
  bot_dir = os.path.dirname(work_dir)
  if os.path.isfile(isolated_result):
    os.remove(isolated_result)
  cmd = []

  # Isolated options.
  if task_details.isolated:
    cmd.extend(
        [
          '-I', task_details.isolated['server'].encode('utf-8'),
          '--namespace', task_details.isolated['namespace'].encode('utf-8'),
        ])
    isolated_input = task_details.isolated.get('input')
    if isolated_input:
      cmd.extend(
          [
            '--isolated', isolated_input,
          ])

  # Named caches options.
  # Specify --named-cache-root unconditionally so run_isolated.py never creates
  # "named_caches" dir and always operats in "c" dir.
  cmd.extend(['--named-cache-root', os.path.join(bot_dir, 'c')])
  if task_details.caches:
    for c in task_details.caches:
      cmd.extend(['--named-cache', c['name'], c['path'].replace('/', os.sep)])

  # Expected output files:
  for output in task_details.outputs:
    cmd.extend(['--output', output])

  # CIPD options. Empty 'packages' list is fine. It means the task needs
  # a bootstrapped CIPD client only.
  if task_details.cipd_input:
    cmd.append('--cipd-enabled')
    for pkg in task_details.cipd_input.get('packages', []):
      cmd.extend([
        '--cipd-package',
        '%s:%s:%s' % (pkg['path'], pkg['package_name'], pkg['version'])])
    cmd.extend(
        [
          '--cipd-cache', os.path.join(bot_dir, 'cipd_cache'),
          '--cipd-client-package',
          task_details.cipd_input['client_package']['package_name'],
          '--cipd-client-version',
          task_details.cipd_input['client_package']['version'],
          '--cipd-server', task_details.cipd_input.get('server'),
        ])

  cmd.extend(
      [
        # Switch to 'task' logical account, if it is set.
        '--switch-to-account', 'task',
        # Cleanup has been run at bot startup in bot_main.py.
        '--no-clean',
        # https://github.com/luci/luci-py/issues/270
        #'--use-symlinks',
        '--json', isolated_result,
        '--log-file', os.path.join(bot_dir, 'logs', 'run_isolated.log'),
        '--root-dir', work_dir,
      ])
  if bot_file:
    cmd.extend(('--bot-file', bot_file))

  if task_details.hard_timeout:
    cmd.extend(('--hard-timeout', str(task_details.hard_timeout)))
  if task_details.grace_period:
    cmd.extend(('--grace-period', str(task_details.grace_period)))

  cmd.extend(run_isolated_flags)

  for key, values in task_details.env_prefixes.iteritems():
    for v in values:
      cmd.extend(('--env-prefix', '%s=%s' % (key, v)))

  # TODO(nodir): Pass the command line arguments via a response file.
  if task_details.command:
    cmd.append('--raw-cmd')
    cmd.append('--')
    cmd.extend(task_details.command)
  elif task_details.extra_args:
    cmd.append('--')
    cmd.extend(task_details.extra_args)
  return cmd


class TaskDetails(object):
  def __init__(self, data):
    logging.info('TaskDetails(%s)', data)
    if not isinstance(data, dict):
      raise InternalError('Expected dict in task_runner_in.json, got %r' % data)

    # Get all the data first so it fails early if the task details is invalid.
    self.bot_id = data['bot_id']

    # Raw command. Only self.command or self.isolated.input can be set.
    self.command = data['command'] or []

    # Isolated command. Is a serialized version of task_request.FilesRef.
    self.isolated = data['isolated']
    self.extra_args = data['extra_args']

    self.cipd_input = data.get('cipd_input')

    self.caches = data.get('caches')

    self.env = {
      k.encode('utf-8'): v.encode('utf-8') for k, v in data['env'].iteritems()
    }
    self.env_prefixes = {
      k.encode('utf-8'): [path.encode('utf-8') for path in v]
      for k, v in (data.get('env_prefixes') or {}).iteritems()
    }
    self.grace_period = data['grace_period']
    self.hard_timeout = data['hard_timeout']
    self.io_timeout = data['io_timeout']
    self.task_id = data['task_id']
    self.outputs = data.get('outputs', [])
    self.secret_bytes = data.get('secret_bytes')

  @staticmethod
  def load(path):
    """Loads the TaskDetails from a file on disk (specified via --in-file).

    Raises InternalError if the file can't be read or parsed.
    """
    try:
      with open(path, 'rb') as f:
        return TaskDetails(json.load(f))
    except (IOError, ValueError) as e:
      raise InternalError('Cannot load task_runner_in.json: %s' % e)


class ExitSignal(Exception):
  """Raised on a signal that the process must exit immediately."""
  def __init__(self, sig):
    super(ExitSignal, self).__init__(u'task_runner received signal %s' % sig)
    self.signal = sig


class InternalError(Exception):
  """Raised on unrecoverable errors that abort task with 'internal error'."""


def load_and_run(
    in_file, swarming_server, is_grpc, cost_usd_hour, start, out_file,
    run_isolated_flags, bot_file, auth_params_file):
  """Loads the task's metadata, prepares auth environment and executes the task.

  This may throw all sorts of exceptions in case of failure. It's up to the
  caller to trap them. These shall be considered 'internal_failure' instead of
  'failure' from a TaskRunResult standpoint.
  """
  auth_system = None
  local_auth_context = None
  task_result = None
  work_dir = os.path.dirname(out_file)

  def handler(sig, _):
    logging.info('Got signal %s', sig)
    raise ExitSignal(sig)

  try:
    with subprocess42.set_signal_handler([SIG_BREAK_OR_TERM], handler):
      # The work directory is guaranteed to exist since it was created by
      # bot_main.py and contains the manifest. Temporary files will be
      # downloaded there. It's bot_main.py that will delete the directory
      # afterward. Tests are not run from there.
      if not os.path.isdir(work_dir):
        raise InternalError('%s expected to exist' % work_dir)

      # Raises InternalError on errors.
      task_details = TaskDetails.load(in_file)

      # This will start a thread that occasionally reads bot authentication
      # headers from 'auth_params_file'. It will also optionally launch local
      # HTTP server that serves OAuth tokens to the task processes. We put
      # location of this service into a file referenced by LUCI_CONTEXT env var
      # below.
      if auth_params_file:
        try:
          auth_system = bot_auth.AuthSystem(auth_params_file)
          local_auth_context = auth_system.start()
        except bot_auth.AuthSystemError as e:
          raise InternalError('Failed to init auth: %s' % e)

      # Override LUCI_CONTEXT['local_auth']. If the task is not using auth,
      # do NOT inherit existing local_auth (if its there). Kick it out by
      # passing None.
      context_edits = {
        'local_auth': local_auth_context
      }

      # Extend existing LUCI_CONTEXT['swarming'], if any.
      if task_details.secret_bytes is not None:
        swarming = luci_context.read('swarming') or {}
        swarming['secret_bytes'] = task_details.secret_bytes
        context_edits['swarming'] = swarming

      # Returns bot authentication headers dict or raises InternalError.
      def headers_cb():
        try:
          if auth_system:
            return auth_system.get_bot_headers()
          return (None, None) # A timeout of "None" means "don't use auth"
        except bot_auth.AuthSystemError as e:
          raise InternalError('Failed to grab bot auth headers: %s' % e)

      # Make a client that can send request to Swarming using bot auth headers.
      grpc_proxy = ''
      if is_grpc:
        grpc_proxy = swarming_server
        swarming_server = ''
      remote = remote_client.createRemoteClient(
          swarming_server, headers_cb, grpc_proxy)
      remote.initialize()

      # Let AuthSystem know it can now send RPCs to Swarming (to grab OAuth
      # tokens). There's a circular dependency here! AuthSystem will be
      # indirectly relying on its own 'get_bot_headers' method to authenticate
      # RPCs it sends through the provided client.
      if auth_system:
        auth_system.set_remote_client(remote)

      # Auth environment is up, start the command. task_result is dumped to
      # disk in 'finally' block.
      with luci_context.stage(_tmpdir=work_dir, **context_edits) as ctx_file:
        task_result = run_command(
            remote, task_details, work_dir, cost_usd_hour,
            start, run_isolated_flags, bot_file, ctx_file)
  except (ExitSignal, InternalError, remote_client.InternalError) as e:
    # This normally means run_command() didn't get the chance to run, as it
    # itself traps exceptions and will report accordingly. In this case, we want
    # the parent process to send the message instead.
    if not task_result:
      task_result = {
        u'exit_code': -1,
        u'hard_timeout': False,
        u'io_timeout': False,
        u'must_signal_internal_failure': str(e.message or 'unknown error'),
        u'version': OUT_VERSION,
      }

  finally:
    # We've found tests to delete the working directory work_dir when quitting,
    # causing an exception here. Try to recreate the directory if necessary.
    if not os.path.isdir(work_dir):
      os.mkdir(work_dir)
    if auth_system:
      auth_system.stop()
    with open(out_file, 'wb') as f:
      json.dump(task_result, f)


def should_post_update(stdout, now, last_packet):
  """Returns True if it's time to send a task_update packet via post_update().

  Sends a packet when one of this condition is met:
  - more than MAX_CHUNK_SIZE of stdout is buffered.
  - last packet was sent more than MIN_PACKET_INTERNAL seconds ago and there was
    stdout.
  - last packet was sent more than MAX_PACKET_INTERVAL seconds ago.
  """
  packet_interval = MIN_PACKET_INTERNAL if stdout else MAX_PACKET_INTERVAL
  return len(stdout) >= MAX_CHUNK_SIZE or (now - last_packet) > packet_interval


def calc_yield_wait(task_details, start, last_io, timed_out, stdout):
  """Calculates the maximum number of seconds to wait in yield_any()."""
  now = monotonic_time()
  if timed_out:
    # Give a |grace_period| seconds delay.
    if task_details.grace_period:
      return max(now - timed_out - task_details.grace_period, 0.)
    return 0.

  out = MIN_PACKET_INTERNAL if stdout else MAX_PACKET_INTERVAL
  if task_details.hard_timeout:
    out = min(out, start + task_details.hard_timeout - now)
  if task_details.io_timeout:
    out = min(out, last_io + task_details.io_timeout - now)
  out = max(out, 0)
  logging.debug('calc_yield_wait() = %d', out)
  return out


def kill_and_wait(proc, grace_period, reason):
  logging.warning('SIGTERM finally due to %s', reason)
  proc.terminate()
  try:
    proc.wait(grace_period)
  except subprocess42.TimeoutError:
    logging.warning('SIGKILL finally due to %s', reason)
    proc.kill()
  exit_code = proc.wait()
  logging.info('Waiting for process exit in finally - done')
  return exit_code


def fail_without_command(remote, bot_id, task_id, params, cost_usd_hour,
                         task_start, exit_code, stdout):
  now = monotonic_time()
  params['cost_usd'] = cost_usd_hour * (now - task_start) / 60. / 60.
  params['duration'] = now - task_start
  params['io_timeout'] = False
  params['hard_timeout'] = False
  # Ignore server reply to stop.
  remote.post_task_update(task_id, bot_id, params, (stdout, 0), 1)
  return {
    u'exit_code': exit_code,
    u'hard_timeout': False,
    u'io_timeout': False,
    u'must_signal_internal_failure': None,
    u'version': OUT_VERSION,
  }


def run_command(remote, task_details, work_dir, cost_usd_hour,
                task_start, run_isolated_flags, bot_file, ctx_file):
  """Runs a command and sends packets to the server to stream results back.

  Implements both I/O and hard timeouts. Sends the packets numbered, so the
  server can ensure they are processed in order.

  Returns:
    Metadata dict with the execution result.

  Raises:
    ExitSignal if caught some signal when starting or stopping.
    InternalError on unexpected internal errors.
  """
  # TODO(maruel): This function is incomprehensible, split and refactor.

  # Signal the command is about to be started. It is important to post a task
  # update *BEFORE* starting any user code to signify the server that the bot
  # correctly started processing the task. In the case of non-idempotent task,
  # this signal is used to know if it is safe to retry the task or not. See
  # _reap_task() in task_scheduler.py for more information.
  last_packet = start = now = monotonic_time()
  task_id = task_details.task_id
  bot_id = task_details.bot_id
  params = {
    'cost_usd': cost_usd_hour * (now - task_start) / 60. / 60.,
  }
  if not remote.post_task_update(task_id, bot_id, params):
    # Don't even bother, the task was already canceled.
    return {
      u'exit_code': -1,
      u'hard_timeout': False,
      u'io_timeout': False,
      u'must_signal_internal_failure': None,
      u'version': OUT_VERSION,
    }

  isolated_result = os.path.join(work_dir, 'isolated_result.json')
  args_path = os.path.join(work_dir, 'run_isolated_args.json')
  cmd = get_run_isolated()
  cmd.extend(['-a', args_path])
  args = get_isolated_args(work_dir, task_details,
                           isolated_result, bot_file, run_isolated_flags)
  # Hard timeout enforcement is deferred to run_isolated. Grace is doubled to
  # give one 'grace_period' slot to the child process and one slot to upload
  # the results back.
  task_details.hard_timeout = 0
  if task_details.grace_period:
    task_details.grace_period *= 2

  try:
    # TODO(maruel): Support both channels independently and display stderr in
    # red.
    env = os.environ.copy()
    for key, value in (task_details.env or {}).iteritems():
      if not value:
        env.pop(key, None)
      else:
        env[key] = value
    if ctx_file:
      env['LUCI_CONTEXT'] = ctx_file
    logging.info('cmd=%s', cmd)
    logging.info('cwd=%s', work_dir)
    logging.info('env=%s', env)
    logging.info('args=%s', args)
    fail_on_start = lambda exit_code, stdout: fail_without_command(
        remote, bot_id, task_id, params, cost_usd_hour, task_start,
        exit_code, stdout)

    # We write args to a file since there may be more of them than the OS
    # can handle.
    try:
      with open(args_path, 'wb') as f:
        json.dump(args, f)
    except (IOError, OSError) as e:
      return fail_on_start(
          -1,
          'Could not write args to %s: %s' % (args_path, e))

    # Start the command
    try:
      assert cmd and all(isinstance(a, basestring) for a in cmd)
      proc = subprocess42.Popen(
          cmd,
          env=env,
          cwd=work_dir,
          detached=True,
          stdout=subprocess42.PIPE,
          stderr=subprocess42.STDOUT,
          stdin=subprocess42.PIPE)
    except OSError as e:
      return fail_on_start(
          1,
          'Command "%s" failed to start.\nError: %s' % (' '.join(cmd), e))

    # Monitor the task
    output_chunk_start = 0
    stdout = ''
    exit_code = None
    had_io_timeout = False
    must_signal_internal_failure = None
    kill_sent = False
    timed_out = None
    try:
      calc = lambda: calc_yield_wait(
          task_details, start, last_io, timed_out, stdout)
      maxsize = lambda: MAX_CHUNK_SIZE - len(stdout)
      last_io = monotonic_time()
      for _, new_data in proc.yield_any(maxsize=maxsize, timeout=calc):
        now = monotonic_time()
        if new_data:
          stdout += new_data
          last_io = now

        # Post update if necessary.
        if should_post_update(stdout, now, last_packet):
          last_packet = monotonic_time()
          params['cost_usd'] = (
              cost_usd_hour * (last_packet - task_start) / 60. / 60.)
          if not remote.post_task_update(
              task_id, bot_id,
              params, (stdout, output_chunk_start)):
            # Server is telling us to stop. Normally task cancellation.
            if not kill_sent:
              logging.warning('Server induced stop; sending SIGKILL')
              proc.kill()
              kill_sent = True

          output_chunk_start += len(stdout)
          stdout = ''

        # Send signal on timeout if necessary. Both are failures, not
        # internal_failures.
        # Eventually kill but return 0 so bot_main.py doesn't cancel the task.
        if not timed_out:
          if (task_details.io_timeout and
              now - last_io > task_details.io_timeout):
            had_io_timeout = True
            logging.warning(
                'I/O timeout is %.3fs; no update for %.3fs sending SIGTERM',
                task_details.io_timeout, now - last_io)
            proc.terminate()
            timed_out = monotonic_time()
        else:
          # During grace period.
          if not kill_sent and now - timed_out >= task_details.grace_period:
            # Now kill for real. The user can distinguish between the following
            # states:
            # - signal but process exited within grace period,
            #   (hard_|io_)_timed_out will be set but the process exit code will
            #   be script provided.
            # - processed exited late, exit code will be -9 on posix.
            logging.warning(
                'Grace of %.3fs exhausted at %.3fs; sending SIGKILL',
                task_details.grace_period, now - timed_out)
            proc.kill()
            kill_sent = True
      logging.info('Waiting for process exit')
      exit_code = proc.wait()
    except (
        ExitSignal, InternalError, IOError,
        OSError, remote_client.InternalError) as e:
      # Something wrong happened, try to kill the child process.
      must_signal_internal_failure = str(e.message or 'unknown error')
      exit_code = kill_and_wait(proc, task_details.grace_period, e.message)

    # This is the very last packet for this command. It if was an isolated task,
    # include the output reference to the archived .isolated file.
    now = monotonic_time()
    params['cost_usd'] = cost_usd_hour * (now - task_start) / 60. / 60.
    params['duration'] = now - start
    params['io_timeout'] = had_io_timeout
    had_hard_timeout = False
    try:
      if not os.path.isfile(isolated_result):
        # It's possible if
        # - run_isolated.py did not start
        # - run_isolated.py started, but arguments were invalid
        # - host in a situation unable to fork
        # - grand child process outliving the child process deleting everything
        #   it can
        # Do not create an internal error, just send back the (partial)
        # view as task_runner saw it, for example the real exit_code is
        # unknown.
        logging.warning('there\'s no result file')
        if exit_code is None:
          exit_code = -1
      else:
        # See run_isolated.py for the format.
        with open(isolated_result, 'rb') as f:
          run_isolated_result = json.load(f)
        logging.debug('run_isolated:\n%s', run_isolated_result)
        # TODO(maruel): Grab statistics (cache hit rate, data downloaded,
        # mapping time, etc) from run_isolated and push them to the server.
        if run_isolated_result['outputs_ref']:
          params['outputs_ref'] = run_isolated_result['outputs_ref']
        had_hard_timeout = run_isolated_result['had_hard_timeout']
        if not had_io_timeout and not had_hard_timeout:
          if run_isolated_result['internal_failure']:
            must_signal_internal_failure = (
                run_isolated_result['internal_failure'])
            logging.error('%s', must_signal_internal_failure)
          elif exit_code:
            # TODO(maruel): Grab stdout from run_isolated.
            must_signal_internal_failure = (
                'run_isolated internal failure %d' % exit_code)
            logging.error('%s', must_signal_internal_failure)
        exit_code = run_isolated_result['exit_code']
        params['bot_overhead'] = 0.
        if run_isolated_result.get('duration') is not None:
          # Calculate the real task duration as measured by run_isolated and
          # calculate the remaining overhead.
          params['bot_overhead'] = params['duration']
          params['duration'] = run_isolated_result['duration']
          params['bot_overhead'] -= params['duration']
          params['bot_overhead'] -= run_isolated_result.get(
              'download', {}).get('duration', 0)
          params['bot_overhead'] -= run_isolated_result.get(
              'upload', {}).get('duration', 0)
          params['bot_overhead'] -= run_isolated_result.get(
              'cipd', {}).get('duration', 0)
          if params['bot_overhead'] < 0:
            params['bot_overhead'] = 0
        isolated_stats = run_isolated_result.get('stats', {}).get('isolated')
        if isolated_stats:
          params['isolated_stats'] = isolated_stats
        cipd_stats = run_isolated_result.get('stats', {}).get('cipd')
        if cipd_stats:
          params['cipd_stats'] = cipd_stats
        cipd_pins = run_isolated_result.get('cipd_pins')
        if cipd_pins:
          params['cipd_pins'] = cipd_pins
    except (IOError, OSError, ValueError) as e:
      logging.error('Swallowing error: %s', e)
      if not must_signal_internal_failure:
        must_signal_internal_failure = '%s\n%s' % (
            e, traceback.format_exc()[-2048:])

    # TODO(maruel): Send the internal failure here instead of sending it through
    # bot_main, this causes a race condition.
    if exit_code is None:
      exit_code = -1
    params['hard_timeout'] = had_hard_timeout

    # Ignore server reply to stop. Also ignore internal errors here if we are
    # already handling some.
    try:
      remote.post_task_update(
          task_id, bot_id, params, (stdout, output_chunk_start), exit_code)
    except remote_client.InternalError as e:
      logging.error('Internal error while finishing the task: %s', e)
      if not must_signal_internal_failure:
        must_signal_internal_failure = str(e.message or 'unknown error')

    return {
      u'exit_code': exit_code,
      u'hard_timeout': had_hard_timeout,
      u'io_timeout': had_io_timeout,
      u'must_signal_internal_failure': must_signal_internal_failure,
      u'version': OUT_VERSION,
    }
  finally:
    file_path.try_remove(unicode(isolated_result))


def main(args):
  subprocess42.inhibit_os_error_reporting()

  # Disable magical auto-detection of OAuth config. See main() in bot_main.py
  # for detailed explanation why.
  net.disable_oauth_config()

  parser = optparse.OptionParser(description=sys.modules[__name__].__doc__)
  parser.add_option('--in-file', help='Name of the request file')
  parser.add_option(
      '--out-file', help='Name of the JSON file to write a task summary to')
  parser.add_option(
      '--swarming-server', help='Swarming server to send data back')
  parser.add_option(
      '--is-grpc', action='store_true',
      help='If true, --swarming-server is a gRPC proxy')
  parser.add_option(
      '--cost-usd-hour', type='float', help='Cost of this VM in $/h')
  parser.add_option('--start', type='float', help='Time this task was started')
  parser.add_option(
      '--bot-file', help='Path to a file describing the state of the host.')
  parser.add_option(
      '--auth-params-file',
      help='Path to a file with bot authentication parameters')

  options, args = parser.parse_args(args)
  if not options.in_file or not options.out_file:
    parser.error('task_runner is meant to be used by swarming_bot.')

  on_error.report_on_exception_exit(options.swarming_server)

  logging.info('starting')
  now = monotonic_time()
  if options.start > now:
    options.start = now

  try:
    load_and_run(
        options.in_file, options.swarming_server, options.is_grpc,
        options.cost_usd_hour, options.start, options.out_file,
        args, options.bot_file, options.auth_params_file)
    return 0
  finally:
    logging.info('quitting')
