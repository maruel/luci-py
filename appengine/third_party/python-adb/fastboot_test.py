# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for adb.fastboot."""

from __future__ import absolute_import

import io
import logging
import os
import sys
import tempfile
import unittest

import common_mock

from adb import adb_protocol
from adb import fastboot


def _SumLengths(items):
  return sum(len(item) for item in items)


class FastbootTest(unittest.TestCase):

  def setUp(self):
    super(FastbootTest, self).setUp()
    self.usb = common_mock.MockUsb()

  def tearDown(self):
    try:
      self.usb.Close()
    finally:
      super(FastbootTest, self).tearDown()

  def ExpectDownload(self, writes, succeed=True):
    self.usb.ExpectWrite(b'download:%08x' % _SumLengths(writes))
    self.usb.ExpectRead(b'DATA%08x' % _SumLengths(writes))

    for data in writes:
      self.usb.ExpectWrite(data)

    if succeed:
      self.usb.ExpectRead(b'OKAYResult')
    else:
      self.usb.ExpectRead(b'FAILResult')

  def ExpectFlash(self, partition, succeed=True):
    self.usb.ExpectWrite(b'flash:%s' % partition)
    self.usb.ExpectRead(b'INFORandom info from the bootloader')
    if succeed:
      self.usb.ExpectRead(b'OKAYDone')
    else:
      self.usb.ExpectRead(b'FAILDone')

  def testDownload(self):
    raw = b'aoeuidhtnsqjkxbmwpyfgcrl'
    data = io.BytesIO(raw)
    self.ExpectDownload([raw])

    commands = fastboot.FastbootCommands(self.usb)
    response = commands.Download(data)
    self.assertEqual(b'Result', response)

  def testDownloadFail(self):
    raw = b'aoeuidhtnsqjkxbmwpyfgcrl'
    data = io.BytesIO(raw)
    self.ExpectDownload([raw], succeed=False)

    commands = fastboot.FastbootCommands(self.usb)
    with self.assertRaises(fastboot.FastbootRemoteFailure):
      commands.Download(data)

    self.usb.ExpectWrite(b'download:%08x' % _SumLengths([raw]))
    self.usb.ExpectRead(b'DATA%08x' % (_SumLengths([raw]) - 2))

    with self.assertRaises(fastboot.FastbootTransferError):
      commands.Download(io.BytesIO(raw))

  def testFlash(self):
    partition = b'yarr'
    self.ExpectFlash(partition)

    commands = fastboot.FastbootCommands(self.usb)
    output = io.BytesIO()
    def InfoCb(message):
      if message.header == b'INFO':
        output.write(message.message)
    response = commands.Flash(partition, info_cb=InfoCb)
    self.assertEqual(b'Done', response)
    self.assertEqual(b'Random info from the bootloader', output.getvalue())

  def testFlashFail(self):
    partition = b'matey'
    self.ExpectFlash(partition, succeed=False)

    commands = fastboot.FastbootCommands(self.usb)
    with self.assertRaises(fastboot.FastbootRemoteFailure):
      commands.Flash(partition)

  def testFlashFromFile(self):
    partition = b'somewhere'
    # More than one packet, ends somewhere into the 3rd packet.
    raw = b'SOMETHING' * 1086
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(raw)
    tmp.close()
    progresses = []

    pieces = []
    chunk_size = fastboot.FASTBOOT_WRITE_CHUNK_SIZE_KB * 1024
    while raw:
      pieces.append(raw[:chunk_size])
      raw = raw[chunk_size:]
    self.ExpectDownload(pieces)
    self.ExpectFlash(partition)

    cb = lambda progress, total: progresses.append((progress, total))

    commands = fastboot.FastbootCommands(self.usb)
    commands.FlashFromFile(
        partition, tmp.name, progress_callback=cb)
    self.assertEqual(len(pieces), len(progresses))
    os.remove(tmp.name)

  def testSimplerCommands(self):
    commands = fastboot.FastbootCommands(self.usb)

    self.usb.ExpectWrite(b'erase:vector')
    self.usb.ExpectRead(b'OKAY')
    commands.Erase(b'vector')

    self.usb.ExpectWrite(b'getvar:variable')
    self.usb.ExpectRead(b'OKAYstuff')
    self.assertEqual(b'stuff', commands.Getvar('variable'))

    self.usb.ExpectWrite(b'continue')
    self.usb.ExpectRead(b'OKAY')
    commands.Continue()

    self.usb.ExpectWrite(b'reboot')
    self.usb.ExpectRead(b'OKAY')
    commands.Reboot()

    self.usb.ExpectWrite(b'reboot-bootloader')
    self.usb.ExpectRead(b'OKAY')
    commands.RebootBootloader()

    self.usb.ExpectWrite(b'oem a little somethin')
    self.usb.ExpectRead(b'OKAYsomethin')
    self.assertEqual(b'somethin', commands.Oem(b'a little somethin'))

  def testVariousFailures(self):
    commands = fastboot.FastbootCommands(self.usb)

    self.usb.ExpectWrite(b'continue')
    self.usb.ExpectRead(b'BLEH')
    with self.assertRaises(fastboot.FastbootInvalidResponse):
      commands.Continue()

    self.usb.ExpectWrite(b'continue')
    self.usb.ExpectRead(b'DATA000000')
    with self.assertRaises(fastboot.FastbootStateMismatch):
      commands.Continue()


if __name__ == '__main__':
  if '-v' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)  # pragma: no cover
    fastboot._LOG.setLevel(logging.DEBUG)  # pragma: no cover
  else:
    logging.basicConfig(level=logging.ERROR)
  unittest.main()
