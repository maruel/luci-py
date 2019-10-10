# Copyright 2013 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Set of functions to work with GAE SDK tools."""

from __future__ import print_function

import collections
import datetime
import glob
import json
import logging
import math
import os
import re
import subprocess
import sys
import time

from six.moves import urllib


# 'setup_gae_sdk' loads the 'yaml' module and modifies this variable.
yaml = None


# Directory with this file.
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


# Path to a current SDK, set in setup_gae_sdk.
_GAE_SDK_PATH = None

# Advanced log filter to help users
_SWITCH_ADVANCED_FILTER = '''
resource.type="gae_app"
resource.labels.version_id="{version}"
logName="projects/{app_id}/logs/appengine.googleapis.com%2Frequest_log"
severity>=ERROR
NOT "Request was aborted after waiting too long"
'''.strip()


class Error(Exception):
  """Base class for a fatal error."""


class BadEnvironmentError(Error):
  """Raised when required tools or environment are missing."""


class LoginRequiredError(Error):
  """Raised by Application methods if use has to go through login flow."""


def _roll_splits(duration, starting_split=None):
  """Generates (old_weight, new_weight) values for
  `gcloud app services set-traffic`, sleeping in between each yield.

  Yields in max(`duration` / 100, 5 minute) intervals.

  Duration should be the number of seconds we want to do the rolling deployment
  over.

  If starting_split is provided, this will offset the start/end times for the
  yielded splits to pick up from where an aborted (or manual) migration left
  off. e.g. if starting_split is '.25', then this is 50% of the way through
  the migration (due to the migration's quadratic split curve), and so
  yield_splits will start yielding from halfway through the migration.
  """
  interval = max(duration / 100, 5 * 60)
  start = time.time()
  end = start + duration

  if starting_split:
    print('\n' + '=' * 60)
    print('Resuming migration at %.1f%%' % (starting_split * 100))
    offset_seconds = math.sqrt(starting_split) * duration
    start -= offset_seconds
    end -= offset_seconds
    print('%.1fs left to go in this migration' % (end - time.time(),))
    print(('=' * 60) + '\n')

  while True:
    now = time.time()
    if now > end:
      break

    # The potential weight is the number of seconds elapsed divided by the total
    # number of seconds. Because we want to follow a quadratic curve (instead of
    # linear), we square this.
    seconds_elapsed = now - start
    potential_weight = (seconds_elapsed / duration)**2

    # The actual new weight is at least 1%, but never more than 100%.
    new_weight = min(1, max(potential_weight, .01))
    if new_weight >= 1:
      break

    yield 1. - new_weight, new_weight

    duration_left = end - now
    to_sleep = min(interval, duration_left)
    print('sleeping %ss for next split (%.1fs left in migration)\n' %
          (to_sleep, duration_left))
    time.sleep(to_sleep)


def find_gcloud():
  """Searches for 'gcloud' binary returning an absolute path to it.

  Will first search for '<candidate>/gcloud/bin/gcloud' where <candidate> goes
  over all parent directories of this script. Failing that will look for
  'gcloud' binary in PATH.

  Raises BadEnvironmentError error if neither method works.
  """
  binary = 'gcloud'
  if sys.platform == 'win32':
    binary += '.cmd'

  search_dir = TOOLS_DIR
  while True:
    exe_file = os.path.join(search_dir, 'gcloud', 'bin', binary)
    if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
      return os.path.realpath(exe_file)
    prev_dir = search_dir
    search_dir = os.path.dirname(search_dir)
    if search_dir == prev_dir:
      break

  for path in os.environ['PATH'].split(os.pathsep):
    exe_file = os.path.join(path, binary)  # <sdk_root>/bin/gcloud
    if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
      return os.path.realpath(exe_file)

  raise BadEnvironmentError(
      'Can\'t find "gcloud". Install the Google Cloud SDK from '
      'https://cloud.google.com/sdk/')


def find_gae_sdk():
  """Returns the path to GAE portion of Google Cloud SDK or None if not found.

  This is '<sdk_root>/platform/google_appengine'. It is documented here:
  https://cloud.google.com/appengine/docs/standard/python/tools/localunittesting

  It is shared between Python and Go flavors of GAE.
  """
  try:
    gcloud = find_gcloud()
  except BadEnvironmentError:
    return None
  # 'gcloud' is <sdk_root>/bin/gcloud.
  sdk_root = os.path.dirname(os.path.dirname(gcloud))
  gae_sdk = os.path.join(sdk_root, 'platform', 'google_appengine')
  if not os.path.isdir(gae_sdk):
    print(
        '-------------------------------------------------------------------\n'
        'Found Cloud SDK in %s but it doesn\'t have App Engine components.\n'
        'If you want to use this SDK, install necessary components:\n'
        '  gcloud components install app-engine-python app-engine-go\n'
        '-------------------------------------------------------------------' %
        sdk_root,
        file=sys.stderr)
    return None
  return gae_sdk


def find_app_yamls(app_dir):
  """Searches for app.yaml and (module|service)-*.yaml in app_dir.

  Recognizes Python and Go GAE apps.

  Returns:
    List of absolute paths to service yamls.

  Raises:
    ValueError if not a valid GAE app.
  """
  # Look in the root first. It will be in the root dir if this is a Python app
  # or single-service Go app.
  yamls = []
  app_yaml = os.path.join(app_dir, 'app.yaml')
  if os.path.isfile(app_yaml):
    yamls.append(app_yaml)
  yamls.extend(glob.glob(os.path.join(app_dir, 'module-*.yaml')))
  yamls.extend(glob.glob(os.path.join(app_dir, 'service-*.yaml')))
  if yamls:
    return sorted(yamls)

  # Look in per-service subdirectories. Only Go apps are structured like this.
  # See https://cloud.google.com/appengine/docs/go/#Go_Organizing_Go_apps.
  for subdir in os.listdir(app_dir):
    subdir = os.path.join(app_dir, subdir)
    if not os.path.isdir(subdir):
      continue
    app_yaml = os.path.join(subdir, 'app.yaml')
    if os.path.isfile(app_yaml):
      yamls.append(app_yaml)
    yamls.extend(glob.glob(os.path.join(subdir, 'module-*.yaml')))
    yamls.extend(glob.glob(os.path.join(subdir, 'service-*.yaml')))
  if not yamls:
    raise ValueError(
        'Not a GAE application directory, no service *.yaml\'s found: %s' %
        app_dir)

  # There should be one and only one app.yaml.
  app_yamls = [p for p in yamls if os.path.basename(p) == 'app.yaml']
  if not app_yamls:
    raise ValueError(
        'Not a GAE application directory, no app.yaml found: %s' % app_dir)
  if len(app_yamls) > 1:
    raise ValueError(
        'Not a GAE application directory, multiple app.yaml found (%s): %s' %
        (app_yamls, app_dir))
  return sorted(yamls)


def is_app_dir(path):
  """Returns True if |path| is structure like GAE app directory."""
  try:
    find_app_yamls(path)
    return True
  except ValueError:
    return False


def setup_gae_sdk(sdk_path):
  """Modifies sys.path and to be able to use Python portion of GAE SDK.

  Once this is called, other functions from this module know where to find GAE
  SDK and any AppEngine included Python module can be imported. The change is
  global and permanent.
  """
  global _GAE_SDK_PATH
  if _GAE_SDK_PATH:
    return
  _GAE_SDK_PATH = sdk_path

  sys.path.insert(0, sdk_path)
  # Sadly, coverage may inject google.protobuf in the path. Forcibly expulse it.
  if 'google' in sys.modules:
    del sys.modules['google']

  import dev_appserver
  dev_appserver.fix_sys_path()
  for i in sys.path[:]:
    if 'jinja2-2.6' in i:
      sys.path.remove(i)

  # Make 'yaml' variable (defined on top of this module) point to loaded module.
  global yaml
  import yaml as yaml_module
  yaml = yaml_module


ModuleFile = collections.namedtuple('ModuleFile', ['path', 'data'])


class Application(object):
  """Configurable GAE application.

  Can be used to query and change GAE application configuration (default
  serving version, uploaded versions, etc.). Built on top of appcfg.py calls.
  """

  def __init__(self, app_dir, app_id=None, verbose=False):
    """Args:
      app_dir: application directory (should contain app.yaml).
      app_id: application ID to use, or None to use one from app.yaml.
      verbose: if True will run all appcfg.py operations in verbose mode.
    """
    if not _GAE_SDK_PATH:
      raise ValueError('Call setup_gae_sdk first')

    self._gae_sdk = _GAE_SDK_PATH
    self._app_dir = os.path.abspath(app_dir)
    self._app_id = app_id
    self._verbose = verbose

    # Module ID -> (path to YAML, deserialized content of service YAML).
    self._services = {}
    for yaml_path in find_app_yamls(self._app_dir):
      with open(yaml_path) as f:
        data = yaml.load(f)
        # The service ID can be specified in the field "service", or
        # "module" (deprecated name). If not specified at all, then
        # it's the default service.
        service_id = data.get('service', data.get('module', 'default'))
        if service_id in self._services:
          raise ValueError(
              'Multiple *.yaml files define same service %s: %s and %s' %
              (service_id, yaml_path, self._services[service_id].path))
        self._services[service_id] = ModuleFile(yaml_path, data)

    self.dispatch_yaml = os.path.join(app_dir, 'dispatch.yaml')
    if not os.path.isfile(self.dispatch_yaml):
      self.dispatch_yaml = None

    if 'default' not in self._services:
      raise ValueError('Default service is missing')
    if not self.app_id:
      raise ValueError('application ID is neither specified in default '
          'service nor provided explicitly')

    self._cached_get_actives = None

  @property
  def app_dir(self):
    """Absolute path to application directory."""
    return self._app_dir

  @property
  def app_id(self):
    """Application ID as passed to constructor, or as read from app.yaml."""
    return self._app_id or self._services['default'].data.get('application')

  @property
  def services(self):
    """List of service IDs that this application contains."""
    return self._services.keys()

  @property
  def service_yamls(self):
    """List of paths to all service YAMLs.

    The first item is always the path the the default service.
    """
    # app.yaml first; this corresponds to the 'default' service.
    yamls = self._services.copy()
    return [yamls.pop('default').path] + [m.path for m in yamls.values()]

  @property
  def default_service_dir(self):
    """Absolute path to a directory with app.yaml of the default service.

    It's different from app_dir for Go apps. dev_appserver.py searches for
    cron.yaml, index.yaml etc. in this directory.
    """
    return os.path.dirname(self._services['default'].path)

  def run_cmd(self, cmd, cwd=None):
    """Runs subprocess, capturing the output.

    Doesn't close stdin, since gcloud may be asking for user input. If this is
    undesirable (e.g when gae.py is used from scripts), close 'stdin' of gae.py
    process itself.
    """
    logging.debug('Running %s', cmd)
    proc = subprocess.Popen(
        cmd,
        cwd=cwd or self._app_dir,
        stdout=subprocess.PIPE)
    output, _ = proc.communicate()
    if proc.returncode:
      sys.stderr.write('\n' + output + '\n')
      raise subprocess.CalledProcessError(proc.returncode, cmd, output)
    return output

  def run_gcloud(self, args):
    """Runs 'gcloud <args> --project ... --format ...' and parses the output."""
    gcloud = find_gcloud()
    if not is_gcloud_auth_set():
      raise LoginRequiredError('Login first using \'gcloud auth login\'')
    raw = self.run_cmd(
        [gcloud] + args + ['--project', self.app_id, '--format', 'json'])
    try:
      return json.loads(raw)
    except ValueError:
      sys.stderr.write('Failed to decode gcloud output %r as JSON\n' % raw)
      raise

  def list_versions(self):
    """List all uploaded versions.

    Returns:
      Dict {service name -> [list of uploaded versions]}.
    """
    data = self.run_gcloud(['app', 'versions', 'list'])
    per_service = collections.defaultdict(list)
    for deployment in data:
      service = deployment['service'].encode('utf-8')
      version_id = deployment['id'].encode('utf-8')
      per_service[service].append(version_id)
    return dict(per_service)

  def oldest_active_version(self, services=None):
    """Returns the oldest active version of the app, or None if no version
    is active.

    Splits version numbers on '-', converts any decimal portions of the split
    version to an int, then compares the resulting tuples to find the lowest
    one.
    """
    actives = self.get_actives(services)
    if actives:
      return actives[0]['id']
    return None

  def set_default_version(self, version, services=None, roll_duration=None):
    """Switches default version of given |services| to |version|."""
    advanced_filter = _SWITCH_ADVANCED_FILTER.format(
        version=version, app_id=self.app_id)
    url = ('https://console.cloud.google.com/logs/viewer?' +
           urllib.parse.urlencode({
               'project': self.app_id,
               'minLogLevel': 0,
               'customFacets': '',
               'limitCustomFacetWidth': 'true',
               'interval': 'NO_LIMIT',
               'resource': 'gae_app/module_id/backend/version_id/' + version,
               'advancedFilter': advanced_filter,
           }))
    print('Monitor error logs for new version here:', url, '\n')

    services = sorted(services or self.services)
    base_cmd = (['app', 'services', 'set-traffic'] + services +
                ['--quiet', '--split-by', 'cookie', '--splits'])

    from_version = self.oldest_active_version(services)
    if roll_duration and from_version != version:
      if len(set(info['id'] for info in self.get_actives(services))) > 2:
        print('Too many active versions! See `gae active`.')
        raise ValueError('too many active versions')

      previous_split = None
      for info in self.get_actives(services):
        if info['id'] == version:
          split = info['traffic_split']
          if previous_split is None or split < previous_split:
            previous_split = split

      print('Beginning migration, press ctrl-C to cancel and reset to %r' %
            (from_version,))

      try:
        for old, new in _roll_splits(roll_duration, previous_split):
          self.run_gcloud(base_cmd + [
              '%s=%s,%s=%s' % (from_version, old, version, new),
          ])
        self.run_gcloud(base_cmd + ['%s=1' % (version,)])
        print('\nMigration complete!')
        return
      except KeyboardInterrupt:
        logging.error('Got KeyboardInterrupt: rolling back')
        version = from_version

    # There's 'versions migrate' command. Unfortunately it requires enabling
    # warmup requests for all services if at least one service has it, which is
    # very inconvenient. Use 'services set-traffic' instead that is free of this
    # weird restriction. If a gradual traffic migration is desired, users can
    # click buttons in Cloud Console.
    self.run_gcloud(base_cmd + ['%s=1' % version])

  def delete_version(self, version, services=None):
    """Deletes the specified version of the given service names."""
    # If --service is not specified, gcloud deletes the version from all
    # services. That's what we want if services is None. --quiet is needed to
    # skip "Do you want to continue?". We've already asked in gae.py.
    if services is None:
      self.run_gcloud(['app', 'versions', 'delete', version, '--quiet'])
    else:
      # Otherwise delete service-by-service.
      for m in sorted(services):
        self.run_gcloud([
          'app', 'versions', 'delete', version, '--service', m, '--quiet'
        ])

  def update(self, version, services=None):
    """Deploys a new version of the given services.

    Supports only GAE Standard currently.
    """
    mods = []
    try:
      for m in sorted(services or self.services):
        mod = self._services[m]
        if mod.data.get('runtime') == 'go' and not os.environ.get('GOROOT'):
          raise BadEnvironmentError('GOROOT must be set when deploying Go app')
        mods.append(mod)
    except KeyError as e:
      raise ValueError('Unknown service: %s' % e)

    # Always make 'default' the first service to be uploaded. It is magical,
    # deploying it first "enables" the application, or so it seems.
    mods.sort(key=lambda x: '' if x == 'default' else x)

    # Will contain paths to service YAMLs and to all extra YAMLs, like
    # cron.yaml.
    yamls = []

    # 'gcloud' barfs at 'application' and 'version' fields in app.yaml. Hack
    # them away. Eventually all app.yaml must be updated to not specify
    # 'application' or 'version'.
    hacked = []
    for m in mods:
      stripped = m.data.copy()
      stripped.pop('application', None)
      stripped.pop('version', None)
      if stripped == m.data:
        yamls.append(m.path)  # the original YAML is good enough
      else:
        # Need to write a hacked version, in same directory, so all paths are
        # relative.
        #
        # TODO(vadimsh): Make this a hard error.
        logging.error(
            'Please remove "application" and "version" keys from %s', m.path)
        fname = os.path.basename(m.path)
        hacked_path = os.path.join(os.path.dirname(m.path), '._gae_py_' + fname)
        with open(hacked_path, 'w') as f:
          json.dump(stripped, f)  # JSON is YAML, so whatever
        yamls.append(hacked_path)
        hacked.append(hacked_path)  # to know what to delete later

    # Deploy all other stuff too. 'app deploy' is a polyglot.
    possible_extra = [
      os.path.join(self.default_service_dir, 'index.yaml'),
      os.path.join(self.default_service_dir, 'queue.yaml'),
      os.path.join(self.default_service_dir, 'cron.yaml'),
      os.path.join(self.default_service_dir, 'dispatch.yaml'),
    ]
    for extra in possible_extra:
      if extra and os.path.isfile(extra):
        yamls.append(extra)

    try:
      self.run_gcloud(
          ['app', 'deploy'] + yamls +
          [
            '--version', version, '--quiet',
            '--no-promote', '--no-stop-previous-version',
          ])
    finally:
      for h in hacked:
        os.remove(h)

  def spawn_dev_appserver(self, args, open_ports=False, **kwargs):
    """Launches subprocess with dev_appserver.py.

    Args:
      args: extra arguments to dev_appserver.py.
      open_ports: if True will bind TCP ports to 0.0.0.0 interface.
      kwargs: passed as is to subprocess.Popen.

    Returns:
      Instance of subprocess.Popen.
    """
    cmd = [
      sys.executable,
      os.path.join(self._gae_sdk, 'dev_appserver.py'),
      '--application', self.app_id,
      '--skip_sdk_update_check=yes',
      '--require_indexes=yes',
    ] + self.service_yamls
    if self.dispatch_yaml:
      cmd += [self.dispatch_yaml]
    cmd += args
    if open_ports:
      cmd.extend(('--host', '0.0.0.0', '--admin_host', '0.0.0.0'))
    if self._verbose:
      cmd.extend(('--log_level', 'debug'))
    return subprocess.Popen(cmd, cwd=self.app_dir, **kwargs)

  def run_dev_appserver(self, args, open_ports=False):
    """Runs the application locally via dev_appserver.py.

    Args:
      args: extra arguments to dev_appserver.py.
      open_ports: if True will bind TCP ports to 0.0.0.0 interface.

    Returns:
      dev_appserver.py exit code.
    """
    return self.spawn_dev_appserver(args, open_ports).wait()

  def get_uploaded_versions(self, services=None):
    """Returns list of versions that are deployed to all given |services|.

    If a version is deployed only to one service, it won't be listed. Versions
    are sorted by a version number, oldest first.
    """
    # Build a mapping: version -> list of services that have it.
    versions = collections.defaultdict(list)
    for service, version_list in self.list_versions().items():
      for version in version_list:
        versions[version].append(service)

    # Keep only versions that are deployed to all requested services.
    services = services or self.services
    actual_versions = [
      version for version, services_with_it in versions.items()
      if set(services_with_it).issuperset(services)
    ]

    # Sort by version number (best effort, nonconforming version names will
    # appear first in the list).
    def extract_version_num(version):
      parts = version.split('-', 1)
      try:
        parts[0] = int(parts[0])
      except ValueError:
        pass
      return tuple(parts)
    return sorted(actual_versions, key=extract_version_num)

  def get_actives(self, services=None):
    """Returns active version(s) sorted by smaller version number first.

    Sorted by (service, ALNUM(id)), where `ALNUM` splits the id (once) by '-',
    and turns any numeral sections to int.
    """

    def _sort_key(info):
      toks = info['id'].split('-', 1)
      if len(toks) == 1:
        return (info['service'], info['id'])

      maybe_vers, rest = toks
      try:
        maybe_vers = int(maybe_vers)
      except ValueError:
        pass

      return (info['service'], (maybe_vers, rest))

    if self._cached_get_actives is None:
      data = self.run_gcloud(['app', 'versions', 'list', '--hide-no-traffic'])
      # There's a lot more data, add what's useful in here as needed.
      actives = [{
          'creationTime': service['version']['createTime'],
          'deployer': service['version']['createdBy'],
          'id': service['id'],
          'traffic_split': service['traffic_split'],
          'service': service['service'],
      } for service in data]
      self._cached_get_actives = sorted(actives, key=_sort_key)

    if services:
      return [
          service for service in self._cached_get_actives
          if service['service'] in services
      ]
    return self._cached_get_actives


def setup_env(app_dir, app_id, version, service_id, remote_api=False):
  """Setups os.environ so GAE code works.

  Must be called only after SDK path has been initialized with setup_gae_sdk.
  """
  # GCS library behaves differently when running under remote_api. It uses
  # SERVER_SOFTWARE to figure this out. See cloudstorage/common.py, local_run().
  if remote_api:
    os.environ['SERVER_SOFTWARE'] = 'remote_api'
  else:
    os.environ['SERVER_SOFTWARE'] = 'Development yo dawg/1.0'
  if app_dir:
    app_id = app_id or Application(app_dir).app_id
    version = version or 'default-version'
  if app_id:
    os.environ['APPLICATION_ID'] = app_id
  if version:
    os.environ['CURRENT_VERSION_ID'] = '%s.%d' % (
        version, int(time.time()) << 28)
  if service_id:
    os.environ['CURRENT_MODULE_ID'] = service_id


def add_roll_duration_option(parser):
  parser.set_defaults(roll_duration=None)

  _TIME_RE = re.compile(r'(?:(?P<hour>\d+)h)?(?:(?P<min>\d+)m)?')

  def _opt_callback(option, _opt, value, parser):
    match = _TIME_RE.match(value or '2h')
    if not match:
      raise ValueError(
          "RollDuration: cannot parse duration as NNhNNm: %r" % (value,))

    setattr(
        parser.values, option.dest,
        datetime.timedelta(
            hours=int(match.group('hour') or 0),
            minutes=int(match.group('min') or 0)).total_seconds())

  parser.add_option(
      '--roll-update',
      metavar='duration',
      type='str',
      nargs=1,
      dest='roll_duration',
      action='callback',
      callback=_opt_callback,
      help=('Do a rolling update over over a period of `duration`. The roll '
            'follows a simple quadratic curve and use cookie traffic '
            'distribution (which, for API users, should be the same as random).'
            ' Duration may be specified as "[NNh][NNm]" where N are numbers. '
            'Canceling gae with ctrl-C will immediately switch back to 0% '
            'traffic for the new version.'))


def add_sdk_options(parser, default_app_dir):
  """Adds common command line options used by tools that wrap GAE SDK.

  Args:
    parser: OptionParser to add options to.
    default_app_dir: default value for --app-dir option.
  """
  parser.add_option(
      '-s', '--sdk-path',
      help='Path to GAE SDK (usually <gcloud_root>/platform/google_appengine). '
           'If not set, will try to find by itself.')
  parser.add_option(
      '-p', '--app-dir',
      default=default_app_dir,
      help='Path to application directory with app.yaml.')
  parser.add_option('-A', '--app-id', help='Defaults to name in app.yaml.')
  parser.add_option('-v', '--verbose', action='store_true')


def process_sdk_options(parser, options):
  """Handles values of options added by 'add_sdk_options'.

  Modifies global process state by configuring logging and path to GAE SDK.

  Args:
    parser: OptionParser instance to use to report errors.
    options: parsed options, as returned by parser.parse_args.

  Returns:
    New instance of Application configured based on passed options.
  """
  logging.basicConfig(level=logging.DEBUG if options.verbose else logging.ERROR)

  if not options.app_dir:
    parser.error('--app-dir option is required')
  app_dir = os.path.abspath(options.app_dir)

  sdk_path = options.sdk_path or find_gae_sdk()
  if not sdk_path:
    parser.error('Failed to find the AppEngine SDK. Pass --sdk-path argument.')

  setup_gae_sdk(sdk_path)

  try:
    return Application(app_dir, options.app_id, options.verbose)
  except (Error, ValueError) as e:
    parser.error(str(e))


def confirm(text, app, version, services=None, default_yes=False):
  """Asks a user to confirm the action related to GAE app.

  Args:
    text: actual text of the prompt.
    app: instance of Application.
    version: version or a list of versions to operate upon.
    services: list of services to operate upon (or None for all).

  Returns:
    True on approval, False otherwise.
  """
  print(text)
  print('  Directory: %s' % os.path.basename(app.app_dir))
  print('  App ID:    %s' % app.app_id)
  print('  Version:   %s' % version)
  print('  Services:  %s' % ', '.join(services or app.services))
  if default_yes:
    return raw_input('Continue? [Y/n] ') not in ('n', 'N')
  else:
    return raw_input('Continue? [y/N] ') in ('y', 'Y')


def is_gcloud_auth_set():
  """Returns false if 'gcloud auth login' needs to be run."""
  try:
    # This returns an email address of currently active account or empty string
    # if no account is active.
    output = subprocess.check_output([
      find_gcloud(), 'auth', 'list',
      '--filter=status:ACTIVE', '--format=value(account)',
    ])
    return bool(output.strip())
  except subprocess.CalledProcessError as exc:
    logging.error('Failed to check active gcloud account: %s', exc)
    return False


def setup_gae_env():
  """Sets up App Engine Python test environment by modifying sys.path."""
  sdk_path = find_gae_sdk()
  if not sdk_path:
    raise BadEnvironmentError('Couldn\'t find GAE SDK.')
  setup_gae_sdk(sdk_path)
