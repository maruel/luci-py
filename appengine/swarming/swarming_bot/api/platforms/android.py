# Copyright 2015 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""Android specific utility functions.

This file serves as an API to bot_config.py. bot_config.py can be replaced on
the server to allow additional server-specific functionality.
"""

import logging
import os
import re
import subprocess
import sys

# This file must be imported from swarming_bot.zip (or with '..' in sys.path).
# libusb1 must have been put in the path already.

import adb
import adb.adb_commands


# Find abs path to third_party/ dir in the bot root dir.
import third_party
THIRD_PARTY_DIR = os.path.dirname(os.path.abspath(third_party.__file__))
sys.path.insert(0, os.path.join(THIRD_PARTY_DIR, 'rsa'))
sys.path.insert(0, os.path.join(THIRD_PARTY_DIR, 'pyasn1'))

import rsa

from pyasn1.codec.der import decoder
from pyasn1.type import univ
from rsa import pkcs1


### Private stuff.


# python-rsa lib hashes all messages it signs. ADB does it already, we just
# need to slap a signature on top of already hashed message. Introduce "fake"
# hashing algo for this.
class _Accum(object):
  def __init__(self):
    self._buf = ''
  def update(self, msg):
    self._buf += msg
  def digest(self):
    return self._buf
pkcs1.HASH_METHODS['SHA-1-PREHASHED'] = _Accum
pkcs1.HASH_ASN1['SHA-1-PREHASHED'] = pkcs1.HASH_ASN1['SHA-1']


# Set when ADB is initialized. It contains one or multiple key used to
# authenticate to Android debug protocol (adb).
_ADB_KEYS = None


# Cache of /system/build.prop on Android devices connected to this host.
_BUILD_PROP_ANDROID = {}


def _dumpsys(cmd, arg):
  out = cmd.Shell('dumpsys ' + arg).decode('utf-8', 'replace')
  if out.startswith('Can\'t find service: '):
    return None
  return out


def _parcel_to_list(lines):
  """Parses 'service call' output."""
  out = []
  for line in lines:
    match = re.match(
        '  0x[0-9a-f]{8}\\: ([0-9a-f ]{8}) ([0-9a-f ]{8}) ([0-9a-f ]{8}) '
        '([0-9a-f ]{8}) \'.{16}\'\\)?', line)
    if not match:
      break
    for i in xrange(1, 5):
      group = match.group(i)
      char = group[4:8]
      if char != '    ':
        out.append(char)
      char = group[0:4]
      if char != '    ':
        out.append(char)
  return out


### Public API.


def initialize(pub_key, priv_key):
  """Initialize Android support through adb.

  You can steal pub_key, priv_key pair from ~/.android/adbkey and
  ~/.android/adbkey.pub.
  """
  global _ADB_KEYS
  assert bool(pub_key) == bool(priv_key)
  if _ADB_KEYS is None:
    _ADB_KEYS = []
    if pub_key:
      try:
        _ADB_KEYS.append(PythonRSASigner(pub_key, priv_key))
      except ValueError as exc:
        logging.warning('Ignoring adb private key: %s', exc)

    # Try to add local adb keys if available.
    path = os.path.expanduser('~/.android/adbkey')
    if os.path.isfile(path) and os.path.isfile(path+'.pub'):
      with open(path + '.pub', 'rb') as f:
        pub = f.read()
      with open(path, 'rb') as f:
        priv = f.read()
      try:
        _ADB_KEYS.append(PythonRSASigner(pub, priv))
      except ValueError as exc:
        logging.warning('Ignoring adb private key %s: %s', path, exc)

    if not _ADB_KEYS:
      return False
  else:
    if pub_key:
      logging.warning('initialize() was called repeatedly: ignoring keys')
  return bool(_ADB_KEYS)


class PythonRSASigner(object):
  """Implements adb_protocol.AuthSigner using http://stuvel.eu/rsa."""
  def __init__(self, pub, priv):
    self.priv_key = load_rsa_private_key(priv)
    self.pub_key = pub

  def Sign(self, data):
    return rsa.sign(data, self.priv_key, 'SHA-1-PREHASHED')

  def GetPublicKey(self):
    return self.pub_key


def load_rsa_private_key(pem):
  """PEM encoded PKCS#8 private key -> rsa.PrivateKey."""
  # ADB uses private RSA keys in pkcs#8 format. 'rsa' library doesn't support
  # them natively. Do some ASN unwrapping to extract naked RSA key
  # (in der-encoded form). See https://www.ietf.org/rfc/rfc2313.txt.
  # Also http://superuser.com/a/606266.
  try:
    der = rsa.pem.load_pem(pem, 'PRIVATE KEY')
    keyinfo, _ = decoder.decode(der)
    if keyinfo[1][0] != univ.ObjectIdentifier('1.2.840.113549.1.1.1'):
        raise ValueError('Not a DER-encoded OpenSSL private RSA key')
    private_key_der = keyinfo[2].asOctets()
  except IndexError:
    raise ValueError('Not a DER-encoded OpenSSL private RSA key')
  return rsa.PrivateKey.load_pkcs1(private_key_der, format='DER')


def kill_adb():
  """adb sucks. Kill it with fire."""
  if not adb:
    return
  try:
    subprocess.call(['adb', 'kill-server'])
  except OSError:
    pass
  subprocess.call(['killall', '--exact', 'adb'])


def get_devices():
  """Returns the list of devices available.

  Caller MUST call close_devices(cmds) on the return value.

  Returns one of:
    - dict of {serial_number: adb.adb_commands.AdbCommands}. The value may be
      None if there was an Auth failure.
    - None if adb is unavailable.
  """
  if not adb:
    return None

  cmds = {}
  generator = adb.adb_commands.AdbCommands.Devices()
  while True:
    try:
      # Use manual iterator handling instead of "for handle in generator" to
      # catch USB exception explicitly.
      handle = generator.next()
    except adb.common.usb1.USBErrorOther as e:
      # This happens if the user is not in group plugdev.
      continue
    except StopIteration:
      break

    try:
      handle.Open()
    except adb.common.usb1.USBErrorBusy:
      logging.warning('Got USBErrorBusy for %s. Killing adb', handle.usb_info)
      kill_adb()
      try:
        # If it throws again, it probably means another process
        # holds a handle to the USB ports or group acl (plugdev) hasn't been
        # setup properly.
        handle.Open()
      except adb.common.usb1.USBErrorBusy as e:
        logging.warning(
            'USB port for %s is already open (and failed to kill ADB) '
            'Try rebooting the host: %s', handle.usb_info, e)
        cmds[handle.serial_number] = None
        continue
    except adb.common.usb1.USBErrorAccess as e:
      # Do not try to use serial_number, since we can't even access the port.
      logging.warning(
          'Try rebooting the host: %s: %s', handle.port_path, e)
      cmds['/'.join(map(str, handle.port_path))] = None
      continue

    try:
      # Give 10s for the user to accept the dialog. The best design would be to
      # do a quick check with timeout=100ms and only if the first failed, try
      # again with a long timeout. The goal is not to hang the bots for several
      # minutes when all the devices are unauthenticated.
      # TODO(maruel): A better fix would be to change python-adb to continue the
      # authentication dance from where it stopped. This is left as a follow up.
      cmd = adb.adb_commands.AdbCommands.Connect(
          handle, banner='swarming', rsa_keys=_ADB_KEYS, auth_timeout_ms=10000)
    except adb.usb_exceptions.DeviceAuthError as e:
      logging.warning('AUTH FAILURE: %s: %s', handle.usb_info, e)
      cmd = None
    except adb.usb_exceptions.ReadFailedError as e:
      logging.warning('READ FAILURE: %s: %s', handle.usb_info, e)
      cmd = None
    except adb.usb_exceptions.WriteFailedError as e:
      logging.warning('WRITE FAILURE: %s: %s', handle.usb_info, e)
      cmd = None
    except ValueError as e:
      logging.warning(
          'Trying unpluging and pluging it back: %s: %s', handle.usb_info, e)
      cmd = None

    try:
      serial = handle.serial_number
    except adb.common.libusb1.USBError:
      serial = handle.usb_info
    cmds[serial] = cmd

  # Remove any /system/build.prop cache so if a device is disconnect, reflashed
  # then reconnected, it will likely be refresh properly. The main concern is
  # that the bot didn't have the time to loop once while this is being done.
  # Restarting the bot works fine too.
  for key in _BUILD_PROP_ANDROID.keys():
    if key not in cmds:
      _BUILD_PROP_ANDROID.pop(key)
  return cmds


def close_devices(devices):
  """Closes all devices opened by get_devices()."""
  for device in (devices or {}).itervalues():
    if device:
      device.Close()


def get_build_prop(cmd):
  """Returns the system properties for a device.

  This isn't really changing through the lifetime of a bot. One corner case is
  when the device is flashed or disconnected.
  """
  if cmd.handle.serial_number not in _BUILD_PROP_ANDROID:
    properties = {}
    try:
      out = cmd.Shell('cat /system/build.prop').decode('utf-8')
    except adb.usb_exceptions.ReadFailedError:
      # It's a bit annoying because it means timeout_ms was wasted. Blacklist
      # the device until it is disconnected and reconnected.
      properties = None
    else:
      for line in out.splitlines():
        if line.startswith(u'#') or not line:
          continue
        key, value = line.split(u'=', 1)
        properties[key] = value
    _BUILD_PROP_ANDROID[cmd.handle.serial_number] = properties
  return _BUILD_PROP_ANDROID[cmd.handle.serial_number]


def get_temp(cmd):
  """Returns the device's 2 temperatures if available."""
  temps = []
  for i in xrange(2):
    try:
      temps.append(
          int(cmd.Shell('cat /sys/class/thermal/thermal_zone%d/temp' % i)))
    except ValueError:
      # On other devices, the only real way to read it is via Java
      # developer.android.com/guide/topics/sensors/sensors_environment.html
      pass
  return temps


def get_battery(cmd):
  """Returns details about the battery's state."""
  props = {}
  out = _dumpsys(cmd, 'battery')
  if not out:
    return props
  for line in out.splitlines():
    if line.endswith(u':'):
      continue
    # On Android 4.1.2, it uses "voltage:123" instead of "voltage: 123".
    key, value = line.split(u':', 2)
    props[key.lstrip()] = value.strip()
  out = {u'power': []}
  if props[u'AC powered'] == u'true':
    out[u'power'].append(u'AC')
  if props[u'USB powered'] == u'true':
    out[u'power'].append(u'USB')
  if props.get(u'Wireless powered') == u'true':
    out[u'power'].append(u'Wireless')
  for key in (u'health', u'level', u'status', u'temperature', u'voltage'):
    out[key] = int(props[key])
  return out


def get_cpu_scale(cmd):
  """Returns the CPU scaling factor."""
  mapping = {
    'cpuinfo_max_freq': u'max',
    'cpuinfo_min_freq': u'min',
    'scaling_cur_freq': u'cur',
  }
  return {
    v: cmd.Shell('cat /sys/devices/system/cpu/cpu0/cpufreq/' + k)
    for k, v in mapping.iteritems()
  }


def get_uptime(cmd):
  """Returns the device's uptime in second."""
  return float(cmd.Shell('cat /proc/uptime').split()[1])


def get_disk(cmd):
  """Returns details about the battery's state."""
  props = {}
  out = _dumpsys(cmd, 'diskstats')
  if not out:
    return props
  for line in out.splitlines():
    if line.endswith(u':'):
      continue
    key, value = line.split(u': ', 2)
    match = re.match(u'^(\d+)K / (\d+)K.*', value)
    if match:
      props[key.lstrip()] = {
        'free_mb': round(float(match.group(1)) / 1024., 1),
        'size_mb': round(float(match.group(2)) / 1024., 1),
      }
  return {
    u'cache': props[u'Cache-Free'],
    u'data': props[u'Data-Free'],
    u'system': props[u'System-Free'],
  }


def get_imei(cmd):
  """Returns the phone's IMEI."""
  # Android <5.0.
  out = _dumpsys(cmd, 'iphonesubinfo')
  match = re.search('  Device ID = (.+)$', out)
  if match:
    return match.group(1)

  # Android >= 5.0.
  lines = cmd.Shell('service call iphonesubinfo 1').splitlines()
  if len(lines) >= 4 and lines[0] == 'Result: Parcel(':
    # Process the UTF-16 string.
    chars = _parcel_to_list(lines[1:])[4:-1]
    return u''.join(map(unichr, (int(i, 16) for i in chars)))


def get_ip(cmd):
  """Returns the IP address."""
  # If ever needed, read wifi.interface from /system/build.prop if a device
  # doesn't use wlan0.
  return cmd.Shell('getprop dhcp.wlan0.ipaddress').strip()
