# Copyright 2014 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""OS specific utility functions.

Includes code:
- to declare the current system this code is running under.
- to run a command on user login.
- to restart the host.

This file serves as an API to bot_config.py. bot_config.py can be replaced on
the server to allow additional server-specific functionality.
"""

import ctypes
import getpass
import glob
import hashlib
import json
import logging
import multiprocessing
import os
import pipes
import platform
import re
import signal
import socket
import string
import subprocess
import sys
import tempfile
import time
import urllib2

from api import parallel
from api import platforms
from utils import file_path
from utils import tools


# For compatibility with older bot_config.py files.
cached = tools.cached


# https://cloud.google.com/compute/pricing#machinetype
GCE_MACHINE_COST_HOUR_US = {
  u'n1-standard-1': 0.063,
  u'n1-standard-2': 0.126,
  u'n1-standard-4': 0.252,
  u'n1-standard-8': 0.504,
  u'n1-standard-16': 1.008,
  u'f1-micro': 0.012,
  u'g1-small': 0.032,
  u'n1-highmem-2': 0.148,
  u'n1-highmem-4': 0.296,
  u'n1-highmem-8': 0.592,
  u'n1-highmem-16': 1.184,
  u'n1-highcpu-2': 0.080,
  u'n1-highcpu-4': 0.160,
  u'n1-highcpu-8': 0.320,
  u'n1-highcpu-16': 0.640,
}


# https://cloud.google.com/compute/pricing#machinetype
GCE_MACHINE_COST_HOUR_EUROPE_ASIA = {
  u'n1-standard-1': 0.069,
  u'n1-standard-2': 0.138,
  u'n1-standard-4': 0.276,
  u'n1-standard-8': 0.552,
  u'n1-standard-16': 1.104,
  u'f1-micro': 0.013,
  u'g1-small': 0.0347,
  u'n1-highmem-2': 0.162,
  u'n1-highmem-4': 0.324,
  u'n1-highmem-8': 0.648,
  u'n1-highmem-16': 1.296,
  u'n1-highcpu-2': 0.086,
  u'n1-highcpu-4': 0.172,
  u'n1-highcpu-8': 0.344,
  u'n1-highcpu-16': 0.688,
}


GCE_RAM_GB_PER_CORE_RATIOS = {
  0.9: u'n1-highcpu-',
  3.75: u'n1-standard-',
  6.5: u'n1-highmem-',
}


# https://cloud.google.com/compute/pricing#disk
GCE_HDD_GB_COST_MONTH = 0.04
GCE_SSD_GB_COST_MONTH = 0.17


# https://cloud.google.com/compute/pricing#premiumoperatingsystems
GCE_WINDOWS_COST_CORE_HOUR = 0.04


### Private stuff.


# Used to calculated Swarming bot uptime.
_STARTED_TS = time.time()



def _write(filepath, content):
  """Writes out a file and returns True on success."""
  logging.info('Writing in %s:\n%s', filepath, content)
  try:
    with open(filepath, mode='wb') as f:
      f.write(content)
    return True
  except IOError as e:
    logging.error('Failed to write %s: %s', filepath, e)
    return False


def _safe_read(filepath):
  """Returns the content of the file if possible, None otherwise."""
  try:
    with open(filepath, 'rb') as f:
      return f.read()
  except (IOError, OSError):
    return None


### Public API.


@tools.cached
def get_os_version_number():
  """Returns the normalized OS version number as a string.

  Returns:
    The format depends on the OS:
    - Windows: 5.1, 6.1, etc. There is no way to distinguish between Windows 7
          and Windows Server 2008R2 since they both report 6.1.
    - OSX: 10.7, 10.8, etc.
    - Ubuntu: 12.04, 10.04, etc.
    Others will return None.
  """
  if sys.platform in ('cygwin', 'win32'):
    return platforms.win.get_os_version_number()
  if sys.platform == 'darwin':
    return platforms.osx.get_os_version_number()
  if sys.platform == 'linux2':
    return platforms.linux.get_os_version_number()

  logging.error('Unable to determine platform version')
  return None


@tools.cached
def get_os_version_name():
  """Returns the marketing name on Windows.

  Returns None on other OSes, since it's not problematic there. Having
  dimensions like Trusty or Snow Leopard is not useful.
  """
  if sys.platform == 'win32':
    return platforms.win.get_os_version_name()
  return None


@tools.cached
def get_os_name():
  """Returns standardized OS name.

  Defaults to sys.platform for OS not normalized.

  Returns:
    Windows, Mac, Ubuntu, Raspbian, etc.
  """
  value = {
    'cygwin': u'Windows',
    'darwin': u'Mac',
    'win32': u'Windows',
  }.get(sys.platform)
  if value:
    return value

  if sys.platform == 'linux2':
    # Try to figure out the distro. Supported distros are Debian, Ubuntu,
    # Raspbian.
    # Add support for other OSes as relevant.
    content = _safe_read('/etc/os-release')
    if content:
      os_release = dict(l.split('=', 1) for l in content.splitlines() if l)
      os_id = os_release.get('ID').strip('"')
      # Uppercase the first letter for consistency with the other platforms.
      return unicode(os_id[0].upper() + os_id[1:])

  return unicode(sys.platform)


@tools.cached
def get_cpu_type():
  """Returns the type of processor: arm or x86."""
  machine = platform.machine().lower()
  if machine in ('amd64', 'x86_64', 'i386'):
    return u'x86'
  return unicode(machine)


@tools.cached
def get_cpu_bitness():
  """Returns the number of bits in the CPU architecture as a str: 32 or 64.

  Unless someone ported python to PDP-10 or 286.

  Note: this function may return 32 bits on 64 bits OS in case of a 32 bits
  python process.
  """
  if platform.machine().endswith('64'):
    return u'64'
  # TODO(maruel): Work harder to figure out if OS is 64 bits.
  return u'64' if sys.maxsize > 2**32 else u'32'


def get_ip():
  """Returns the IP that is the most likely to be used for TCP connections."""
  # Tries for ~0.5s then give up.
  max_tries = 10
  for i in xrange(10):
    # It's guesswork and could return the wrong IP. In particular a host can
    # have multiple IPs.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # This doesn't actually connect to the Google DNS server but this forces the
    # network system to figure out an IP interface to use.
    try:
      s.connect(('8.8.8.8', 80))
      return s.getsockname()[0]
    except socket.error:
      # Can raise "error: [Errno 10051] A socket operation was attempted to an
      # unreachable network" if the network is still booting up. We don't want
      # this function to crash.
      if i == max_tries - 1:
        # Can't determine the IP.
        return '0.0.0.0'
      time.sleep(0.05)
    finally:
      s.close()


def get_hostname():
  """Returns the machine's hostname."""
  # Windows enjoys putting random case in there. Enforces lower case for sanity.
  hostname = socket.getfqdn().lower()
  if hostname.endswith('.in-addr.arpa'):
    # The base name will be the IPv4 address reversed, which is not useful. This
    # happens on OSX.
    hostname = socket.gethostname()
  return unicode(hostname)


def get_hostname_short():
  """Returns the base host name."""
  return get_hostname().split(u'.', 1)[0]


@tools.cached
def get_num_processors():
  """Returns the number of processors.

  Python on OSX 10.6 raises a NotImplementedError exception.
  """
  try:
    # Multiprocessing
    return multiprocessing.cpu_count()
  except:  # pylint: disable=W0702
    try:
      # Mac OS 10.6
      return int(os.sysconf('SC_NPROCESSORS_ONLN'))  # pylint: disable=E1101
    except:
      # Returns non-zero, otherwise it could generate a divide by zero later
      # when doing calculations, leading to a crash. Saw it happens on Win2K8R2
      # on python 2.7.5 on cygwin 1.7.28.
      logging.error('get_num_processors() failed to query number of cores')
      # Return an improbable number to make it easier to catch.
      return 5


@tools.cached
def get_physical_ram():
  """Returns the amount of installed RAM in Mb, rounded to the nearest number.
  """
  if sys.platform == 'win32':
    return platforms.win.get_physical_ram()
  if sys.platform == 'darwin':
    return platforms.osx.get_physical_ram()
  if os.path.isfile('/proc/meminfo'):
    # linux.
    meminfo = _safe_read('/proc/meminfo') or ''
    matched = re.search(r'MemTotal:\s+(\d+) kB', meminfo)
    if matched:
      mb = int(matched.groups()[0]) / 1024.
      if 0. < mb < 1.:
        return 1
      return int(round(mb))

  logging.error('get_physical_ram() failed to query amount of physical RAM')
  return 0


def get_disks_info():
  """Returns a dict of dict of free and total disk space."""
  if sys.platform == 'win32':
    return platforms.win.get_disks_info()
  else:
    return platforms.posix.get_disks_info()


@tools.cached
def get_gpu():
  """Returns the installed video card(s) name.

  Returns:
    All the video cards detected.
    tuple(list(dimensions), list(state)).
  """
  if sys.platform == 'darwin':
    dimensions, state = platforms.osx.get_gpu()
  elif sys.platform == 'linux2':
    dimensions, state = platforms.linux.get_gpu()
  elif sys.platform == 'win32':
    dimensions, state = platforms.win.get_gpu()
  else:
    dimensions, state = None, None

  # 15ad is VMWare. It's akin not having a GPU card.
  dimensions = dimensions or [u'none']
  if '15ad' in dimensions:
    dimensions.append(u'none')
    dimensions.sort()
  return dimensions, state


@tools.cached
def get_monitor_hidpi():
  """Returns True if there is an hidpi monitor detected."""
  if sys.platform == 'darwin':
    return [platforms.osx.get_monitor_hidpi()]
  return None


@tools.cached
def get_cost_hour():
  """Returns the cost in $USD/h as a floating point value if applicable."""
  # Machine.
  machine_type = get_machine_type()
  if platforms.is_gce():
    if platforms.gce.get_zone().startswith('us-'):
      machine_cost = GCE_MACHINE_COST_HOUR_US[machine_type]
    else:
      machine_cost = GCE_MACHINE_COST_HOUR_EUROPE_ASIA[machine_type]
  else:
    # Guess an equivalent machine_type.
    machine_cost = GCE_MACHINE_COST_HOUR_US.get(machine_type, 0.)

  # OS.
  os_cost = 0.
  if sys.platform == 'darwin':
    # Apple tax. It's 50% better, right?
    os_cost = GCE_WINDOWS_COST_CORE_HOUR * 1.5 * get_num_processors()
  elif sys.platform == 'win32':
    # MS tax.
    if machine_type in ('f1-micro', 'g1-small'):
      os_cost = 0.02
    else:
      os_cost = GCE_WINDOWS_COST_CORE_HOUR * get_num_processors()

  # Disk.
  # TODO(maruel): Figure out the disk type. The metadata is not useful AFAIK.
  # Assume HDD for now, it's the cheapest. That's not true, we do have SSDs.
  disk_gb_cost = 0.
  for disk in get_disks_info().itervalues():
    disk_gb_cost += disk['free_mb'] / 1024. * (
        GCE_HDD_GB_COST_MONTH / 30. / 24.)

  # TODO(maruel): Network. It's not a constant cost, it's per task.
  # See https://cloud.google.com/monitoring/api/metrics
  # compute.googleapis.com/instance/network/sent_bytes_count
  return machine_cost + os_cost + disk_gb_cost


@tools.cached
def get_machine_type():
  """Returns a GCE-equivalent machine type.

  If running on GCE, returns the right machine type. Otherwise tries to find the
  'closest' one.
  """
  if platforms.is_gce():
    return platforms.gce.get_machine_type()

  ram_gb = get_physical_ram() / 1024.
  cores = get_num_processors()
  ram_gb_per_core = ram_gb / cores
  logging.info('RAM GB/core = %.3f', ram_gb_per_core)
  best_fit = None
  for ratio, prefix in GCE_RAM_GB_PER_CORE_RATIOS.iteritems():
    delta = (ram_gb_per_core-ratio)**2
    if best_fit is None or delta < best_fit[0]:
      best_fit = (delta, prefix)
  prefix = best_fit[1]
  machine_type = prefix + unicode(cores)
  if machine_type not in GCE_MACHINE_COST_HOUR_US:
    # Try a best fit.
    logging.info('Failed to find a good machine_type match: %s', machine_type)
    for i in (16, 8, 4, 2):
      if cores > i:
        machine_type = prefix + unicode(i)
        break
    else:
      if cores == 1:
        # There's no n1-highcpu-1 nor n1-highmem-1.
        if ram_gb < 1.7:
          machine_type = u'f1-micro'
        elif ram_gb < 3.75:
          machine_type = u'g1-small'
        else:
          machine_type = u'n1-standard-1'
      else:
        logging.info('Failed to find a fit: %s', machine_type)

  if machine_type not in GCE_MACHINE_COST_HOUR_US:
    return None
  return machine_type


@tools.cached
def can_send_metric():
  """True if 'send_metric' really does something."""
  if platforms.is_gce():
    # Scope to use Cloud Monitoring.
    scope = 'https://www.googleapis.com/auth/monitoring'
    return scope in platforms.gce.oauth2_available_scopes()
  return False


def send_metric(name, value):
  if platforms.is_gce():
    return platforms.gce.send_metric(name, value)
  # Ignore on other platforms for now.


### Android.


def get_dimensions_all_devices_android(devices):
  """Returns the default dimensions for an host with multiple android devices.
  """
  dimensions = get_dimensions()
  if not devices:
    return dimensions

  # Pop a few dimensions otherwise there will be too many dimensions.
  del dimensions[u'cpu']
  del dimensions[u'cores']
  del dimensions[u'gpu']
  dimensions.pop(u'machine_type')

  # Make sure all the devices use the same board.
  keys = (u'build.id', u'product.board')
  for key in keys:
    dimensions[key] = set()
  dimensions[u'android'] = []
  for device in devices:
    properties = platforms.android.get_build_prop(device)
    if properties:
      for key in keys:
        real_key = u'ro.' + key
        if real_key in properties:
          dimensions[key].add(properties[real_key])
      # Only advertize devices that can be used.
      dimensions[u'android'].append(device.serial)
  dimensions[u'android'].sort()
  for key in keys:
    if not dimensions[key]:
      del dimensions[key]
    else:
      dimensions[key] = sorted(dimensions[key])
  nb_android = len(dimensions[u'android'])
  dimensions[u'android_devices'] = map(
      str, range(nb_android, max(0, nb_android-2), -1))

  # TODO(maruel): Add back once dimensions limit is figured out and there's a
  # need.
  del dimensions[u'android']
  # Trim 'os' to reduce the number of dimensions and not run tests by accident
  # on it.
  dimensions[u'os'] = ['Android']
  return dimensions


def get_state_all_devices_android(devices):
  """Returns state information about all the devices connected to the host.
  """
  state = get_state()
  if not devices:
    return state

  # Add a few values that were poped from dimensions.
  cpu_type = get_cpu_type()
  cpu_bitness = get_cpu_bitness()
  state[u'cpu'] = [
    cpu_type,
    cpu_type + u'-' + cpu_bitness,
  ]
  state[u'cores'] = [unicode(get_num_processors())]
  state[u'gpu'] = get_gpu()[0]
  machine_type = get_machine_type()
  if machine_type:
    state[u'machine_type'] = [machine_type]

  keys = (
    u'board.platform',
    u'build.fingerprint',
    u'build.id',
    u'build.tags',
    u'build.type',
    u'build.version.release',
    u'build.version.sdk',
    u'product.board',
    u'product.cpu.abi')

  def fn(device):
    if not device.is_valid:
      return {u'state': 'unauthenticated'}
    properties = platforms.android.get_build_prop(device)
    if not properties:
      return {u'state': 'unavailable'}
    return {
      u'battery': platforms.android.get_battery(device),
      u'build': {key: properties[u'ro.'+key] for key in keys},
      u'cpu_scale': platforms.android.get_cpu_scale(device),
      u'disk': platforms.android.get_disk(device),
      u'imei': platforms.android.get_imei(device),
      u'ip': platforms.android.get_ip(device),
      u'max_uid': platforms.android.get_last_uid(device),
      u'other_packages': [
        p for p in platforms.android.list_packages(device) or []
        if not p.startswith(('com.android.', 'com.google.')) and p != 'android'
      ],
      u'serial': device.serial,
      u'state': u'available',
      u'temp': platforms.android.get_temp(device),
      u'uptime': platforms.android.get_uptime(device),
    }

  start = time.time()
  state[u'devices'] = {
    device.port_path: out
    for device, out in zip(devices, parallel.pmap(fn, devices))
  }
  logging.info(
      'get_state_all_devices_android() (device part) took %gs' %
      round(time.time() - start, 1))
  return state


###


def get_dimensions():
  """Returns the default dimensions."""
  os_name = get_os_name()
  cpu_type = get_cpu_type()
  cpu_bitness = get_cpu_bitness()
  dimensions = {
    u'cores': [unicode(get_num_processors())],
    u'cpu': [
      cpu_type,
      cpu_type + u'-' + cpu_bitness,
    ],
    u'gpu': get_gpu()[0],
    u'id': [get_hostname_short()],
    u'os': [os_name],
  }
  os_version_name = get_os_version_name()
  if os_version_name:
    # This only happens on Windows.
    dimensions[u'os'].append(u'%s-%s' % (os_name, os_version_name))
  else:
    dimensions[u'os'].append(u'%s-%s' % (os_name, get_os_version_number()))
  if u'none' not in dimensions[u'gpu']:
    hidpi = get_monitor_hidpi()
    if hidpi:
      dimensions[u'hidpi'] = hidpi

  machine_type = get_machine_type()
  if machine_type:
    dimensions[u'machine_type'] = [machine_type]
  if platforms.is_gce():
    dimensions[u'zone'] = [platforms.gce.get_zone()]

  if cpu_type.startswith(u'arm') and cpu_type != u'arm':
    dimensions[u'cpu'].append(u'arm')
    dimensions[u'cpu'].append(u'arm-' + cpu_bitness)
    dimensions[u'cpu'].sort()

  if sys.platform == 'linux2':
    dimensions[u'os'].append(u'Linux')
    dimensions[u'os'].sort()

  return dimensions


def get_state(threshold_mb=4*1024, skip=None):
  """Returns dict with a state of the bot reported to the server with each poll.

  Supposed to be use only for dynamic state that changes while bot is running.

  The server can not use this state for immediate scheduling purposes (use
  'dimensions' for that), but it can use it for maintenance and bookkeeping
  tasks.

  Arguments:
  - threshold_mb: number of mb below which the bot will quarantine itself
        automatically. Set to 0 or None to disable.
  - skip: list of partitions to skip for automatic quarantining on low free
        space.
  """
  # TODO(vadimsh): Send 'uptime', number of open file descriptors, processes or
  # any other leaky resources. So that the server can decided to reboot the bot
  # to clean up.
  nb_files_in_temp = len(os.listdir(tempfile.gettempdir()))
  state = {
    u'cost_usd_hour': get_cost_hour(),
    u'cwd': os.getcwd(),
    u'disks': get_disks_info(),
    u'gpu': get_gpu()[1],
    u'hostname': get_hostname(),
    u'ip': get_ip(),
    u'nb_files_in_temp': nb_files_in_temp,
    u'ram': get_physical_ram(),
    u'running_time': int(round(time.time() - _STARTED_TS)),
    u'started_ts': int(round(_STARTED_TS)),
  }
  if sys.platform in ('cygwin', 'win32'):
    state[u'cygwin'] = [sys.platform == 'cygwin']
  if sys.platform == 'win32':
    integrity = platforms.win.get_integrity_level()
    if integrity is not None:
      state[u'integrity'] = [integrity]

  # TODO(maruel): Put an arbitrary limit on the amount of junk that can stay in
  # TEMP dir once we eyeballed that not the whole fleet will instantly
  # self-quarantine.
  #if nb_files_in_temp > 1024:
  #  state[u'quarantined'] = '> 1024 files in TEMP'
  auto_quarantine_on_low_space(state, threshold_mb, skip)
  return state


def auto_quarantine_on_low_space(state, threshold_mb, skip=None):
  """Quarantines when less than threshold_mb on any partition.

  Modifies state in-place. Assumes state['free_disks'] is valid.
  """
  if not threshold_mb or state.get(u'quarantined'):
    return
  if skip is None:
    # Do not check these mount points for low disk space.
    skip = ['/boot', '/boot/efi']

  s = []
  for mount, infos in state[u'disks'].iteritems():
    space_mb = infos['free_mb']
    if mount not in skip and space_mb < threshold_mb:
      s.append('Not enough free disk space on %s.' % mount)
  if s:
    state[u'quarantined'] = '\n'.join(s)


def rmtree(path):
  """Removes a directory the bold way."""
  file_path.rmtree(path)


def setup_auto_startup_win(command, cwd, batch_name):
  """Uses Startup folder in the Start Menu.

  This assumes the user is automatically logged in on OS startup.

  Works both inside cygwin's python or native python which makes this function a
  bit more tricky than necessary.

  Use the start up menu instead of registry for two reasons:
  - It's easy to remove in case of failure, for example in case of reboot loop.
  - It works well even with cygwin.

  TODO(maruel): This function assumes |command| is python script to be run.
  """
  logging.info('setup_auto_startup_win(%s, %s, %s)', command, cwd, batch_name)
  if not os.path.isabs(cwd):
    raise ValueError('Refusing relative path')
  assert batch_name.endswith('.bat'), batch_name
  batch_path = platforms.win.get_startup_dir() + batch_name

  # If we are running through cygwin, the path to write to must be changed to be
  # in the cywgin format, but we also need to change the commands to be in
  # non-cygwin format (since they will execute in a batch file).
  if sys.platform == 'cygwin':
    batch_path = platforms.win.to_cygwin_path(batch_path)
    assert batch_path
    cwd = platforms.win.from_cygwin_path(cwd)
    assert cwd

    # Convert all the cygwin paths in the command.
    for i in range(len(command)):
      if '/cygdrive/' in command[i]:
        command[i] = platforms.win.from_cygwin_path(command[i])

  # TODO(maruel): Shell escape! Sadly shlex.quote() is only available starting
  # python 3.3 and it's tricky on Windows with '^'.
  # Don't forget the CRLF, otherwise cmd.exe won't process it.
  content = (
      '@echo off\r\n'
      ':: This file was generated automatically by os_platforms.py.\r\n'
      'cd /d %s\r\n'
      'mkdir logs\n\n'
      '%s 1>> logs\\bot_stdout.log 2>&1\r\n') % (cwd, ' '.join(command))
  success = _write(batch_path, content)
  if success and sys.platform == 'cygwin':
    # For some reason, cygwin tends to create the file with 0644.
    os.chmod(batch_path, 0755)
  return success


def setup_auto_startup_osx(command, cwd, plistname):
  """Uses launchd to start the command when the user logs in.

  This assumes the user is automatically logged in on OS startup.

  In case of failure like reboot loop, simply remove the file in
  ~/Library/LaunchAgents/.
  """
  logging.info('setup_auto_startup_osx(%s, %s, %s)', command, cwd, plistname)
  if not os.path.isabs(cwd):
    raise ValueError('Refusing relative path')
  assert plistname.endswith('.plist'), plistname
  launchd_dir = os.path.expanduser('~/Library/LaunchAgents')
  if not os.path.isdir(launchd_dir):
    # This directory doesn't exist by default.
    # Sometimes ~/Library gets deleted.
    os.makedirs(launchd_dir)
  filepath = os.path.join(launchd_dir, plistname)
  return _write(
      filepath, platforms.osx.generate_launchd_plist(command, cwd, plistname))


def setup_auto_startup_initd_linux(command, cwd, user=None, name='swarming'):
  """Uses init.d to start the bot automatically."""
  if not user:
    user = getpass.getuser()
  logging.info(
      'setup_auto_startup_initd_linux(%s, %s, %s, %s)',
      command, cwd, user, name)
  if not os.path.isabs(cwd):
    raise ValueError('Refusing relative path')
  script = platforms.linux.generate_initd(command, cwd, user)
  filepath = pipes.quote(os.path.join('/etc/init.d', name))
  with tempfile.NamedTemporaryFile() as f:
    if not _write(f.name, script):
      return False

    # Need to do 3 things as sudo. Do it all at once to enable a single sudo
    # request.
    # TODO(maruel): Likely not the sanest thing, reevaluate.
    cmd = [
      'sudo', '/bin/sh', '-c',
      "cp %s %s && chmod 0755 %s && update-rc.d %s defaults" % (
        pipes.quote(f.name), filepath, filepath, name)
    ]
    subprocess.check_call(cmd)
    print('To remove, use:')
    print('  sudo update-rc.d -f %s remove' % name)
    print('  sudo rm %s' % filepath)
  return True


def setup_auto_startup_autostart_desktop_linux(command, name='swarming'):
  """Uses ~/.config/autostart to start automatically the bot on user login.

  http://standards.freedesktop.org/autostart-spec/autostart-spec-latest.html
  """
  basedir = os.path.expanduser('~/.config/autostart')
  if not os.path.isdir(basedir):
    os.makedirs(basedir)
  filepath = os.path.join(basedir, '%s.desktop' % name)
  return _write(
      filepath, platforms.linux.generate_autostart_destkop(command, name))


def restart(message=None, timeout=None):
  """Restarts this machine.

  If it fails to reboot the host, it loops until timeout. This function does
  not return on successful restart, or returns False if machine wasn't
  restarted within |timeout| seconds.
  """
  # The shutdown process sends SIGTERM and waits for processes to exit. It's
  # important to not handle SIGTERM and die when needed.
  signal.signal(signal.SIGTERM, signal.SIG_DFL)

  deadline = time.time() + timeout if timeout else None
  while True:
    restart_and_return(message)
    # Sleep for 300 seconds to ensure we don't try to do anymore work while the
    # OS is preparing to shutdown.
    duration = min(300, deadline - time.time()) if timeout else 300
    if duration > 0:
      logging.info('Sleeping for %s', duration)
      time.sleep(duration)
    if timeout and time.time() >= deadline:
      logging.warning(
          'Waited for host to restart for too long (%s); aborting', timeout)
      return False


def restart_and_return(message=None):
  """Tries to restart this host and immediately return to the caller.

  This is mostly useful when done via remote shell, like via ssh, where it is
  not worth waiting for the TCP connection to tear down.

  Returns:
    True if at least one command succeeded.
  """
  if sys.platform == 'win32':
    cmds = [
      ['shutdown', '-r', '-f', '-t', '1'],
    ]
  elif sys.platform == 'cygwin':
    # The one that will succeed depends if it is executed via a prompt or via
    # a ssh command. #itscomplicated.
    cmds = [
      ['shutdown', '-r', '-f', '-t', '1'],
      ['shutdown', '-r', '-f', '1'],
    ]
  elif sys.platform == 'linux2' or sys.platform == 'darwin':
    cmds = [['sudo', '/sbin/shutdown', '-r', 'now']]
  else:
    cmds = [['sudo', 'shutdown', '-r', 'now']]

  success = False
  for cmd in cmds:
    logging.info(
        'Restarting machine with command %s (%s)', ' '.join(cmd), message)
    try:
      subprocess.check_call(cmd)
      logging.info('Restart command exited successfully')
    except (OSError, subprocess.CalledProcessError) as e:
      logging.error('Failed to run %s: %s', ' '.join(cmd), e)
    else:
      success = True
  return success


def roll_log(name):
  """Rolls a log in 5Mb chunks and keep the last 10 files."""
  try:
    if not os.path.isfile(name) or os.stat(name).st_size < 5*1024*1024:
      return
    if os.path.isfile('%s.9' % name):
      os.remove('%s.9' % name)
    for i in xrange(8, 0, -1):
      item = '%s.%d' % (name, i)
      if os.path.isfile(item):
        os.rename(item, '%s.%d' % (name, i+1))
    if os.path.isfile(name):
      os.rename(name, '%s.1' % name)
  except Exception as e:
    logging.exception('roll_log(%s) failed: %s', name, e)


def trim_rolled_log(name):
  try:
    for item in glob.iglob('%s.??' % name):
      os.remove(item)
    for item in glob.iglob('%s.???' % name):
      os.remove(item)
  except Exception as e:
    logging.exception('trim_rolled_log(%s) failed: %s', name, e)
