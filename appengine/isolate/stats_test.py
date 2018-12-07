#!/usr/bin/env python
# Copyright 2014 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import datetime
import sys
import unittest

# pylint: disable=wrong-import-position
import test_env
test_env.setup_test_env()

import webapp2
import webtest

from components import stats_framework
from components.stats_framework import stats_logs
from test_support import stats_framework_logs_mock
from test_support import test_case

import stats


class Store(webapp2.RequestHandler):
  def get(self):
    """Generates fake stats."""
    stats.add_entry(stats.STORE, 2048, 'GS; inline')
    self.response.write('Yay')


class Return(webapp2.RequestHandler):
  def get(self):
    """Generates fake stats."""
    stats.add_entry(stats.RETURN, 4096, 'memcache')
    self.response.write('Yay')


class Lookup(webapp2.RequestHandler):
  def get(self):
    """Generates fake stats."""
    stats.add_entry(stats.LOOKUP, 200, 103)
    self.response.write('Yay')


class Dupe(webapp2.RequestHandler):
  def get(self):
    """Generates fake stats."""
    stats.add_entry(stats.DUPE, 1024, 'inline')
    self.response.write('Yay')


def to_str(now, delta):
  """Converts a datetime to unicode."""
  now = now + datetime.timedelta(seconds=delta)
  return unicode(now.strftime(stats.utils.DATETIME_FORMAT))


class StatsTest(test_case.TestCase):
  def setUp(self):
    super(StatsTest, self).setUp()
    fake_routes = [
        ('/store', Store),
        ('/return', Return),
        ('/lookup', Lookup),
        ('/dupe', Dupe),
    ]
    self.app = webtest.TestApp(
        webapp2.WSGIApplication(fake_routes, debug=True),
        extra_environ={'REMOTE_ADDR': 'fake-ip'})
    stats_framework_logs_mock.configure(self)
    self.now = datetime.datetime(2010, 1, 2, 3, 4, 5, 6)
    self.mock_now(self.now, 0)

  def test_all_apis_are_tested(self):
    # Ensures there's a test for each public API.
    module = stats
    expected = frozenset(
        i for i in dir(module)
        if i[0] != '_' and hasattr(getattr(module, i), 'func_name'))
    missing = expected - frozenset(
        i[5:] for i in dir(self) if i.startswith('test_'))
    self.assertFalse(missing)

  def _test_handler(self, url, added_data):
    stats_framework_logs_mock.reset_timestamp(stats.STATS_HANDLER, self.now)

    self.assertEqual('Yay', self.app.get(url).body)
    self.assertEqual(1, len(list(stats_logs.yield_entries(None, None))))

    self.mock_now(self.now, 60)
    self.assertEqual(10, stats.cron_generate_stats())

    actual = stats_framework.get_stats(
        stats.STATS_HANDLER, 'minutes', self.now, 1, True)
    expected = [
      {
        'contains_lookups': 0,
        'contains_requests': 0,
        'downloads': 0,
        'downloads_bytes': 0,
        'failures': 0,
        'key': '2010-01-02T03:04',
        'requests': 1,
        'uploads': 0,
        'uploads_bytes': 0,
      },
    ]
    expected[0].update(added_data)
    self.assertEqual(expected, actual)

  def test_store(self):
    expected = {
      'uploads': 1,
      'uploads_bytes': 2048,
    }
    self._test_handler('/store', expected)

  def test_return(self):
    expected = {
      'downloads': 1,
      'downloads_bytes': 4096,
    }
    self._test_handler('/return', expected)

  def test_lookup(self):
    expected = {
      'contains_lookups': 200,
      'contains_requests': 1,
    }
    self._test_handler('/lookup', expected)

  def test_dupe(self):
    expected = {}
    self._test_handler('/dupe', expected)

  def test_add_entry(self):
    # Tested by other test cases.
    pass

  def test_snapshot_to_proto(self):
    # TODO(maruel): Implement.
    pass

  def test_cron_generate_stats(self):
    self.assertEqual(120, stats.cron_generate_stats())

  def test_cron_send_to_bq(self):
    def json_request(url, method, payload, scopes, deadline):
      self.assertEqual(
          'https://www.googleapis.com/bigquery/v2/projects/sample-app/datasets/'
            'isolated/tables/stats/insertAll',
          url)
      self.assertEqual('POST', method)
      self.assertEqual(
          {
            'ignoreUnknownValues': False,
            'kind': 'bigquery#tableDataInsertAllRequest',
            'rows': [],
            'skipInvalidRows': True,
          },
          payload)
      self.assertEqual(stats.helper.INSERT_ROWS_SCOPE, scopes)
      self.assertEqual(600, deadline)
      return {}
    self.mock(stats.net, 'json_request', json_request)
    self.assertEqual([], stats.cron_send_to_bq())


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  unittest.main()
