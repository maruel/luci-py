# Copyright 2014 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""This modules is imported by AppEngine and defines the 'app' object.

It is a separate file so that application bootstrapping code like ereporter2,
that shouldn't be done in unit tests, can be done safely. This file must be
tested via a smoke test.
"""

import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(APP_DIR, 'components', 'third_party'))

from components import utils
utils.fix_protobuf_package()

import endpoints

from components import auth
from components import config
from components import ereporter2

import handlers_frontend
import monitoring


def create_applications():
  ereporter2.register_formatter()

  # App that serves HTML pages and the main API.
  frontend = monitoring.wrap_webapp2_app(
      handlers_frontend.create_application(False))

  # App that serves endpoints APIs. Note: monitoring.wrap_webapp2_app doesn't
  # support Endpoints server. This is fine, we don't host any important APIs
  # there.
  api = endpoints.api_server([auth.AuthService, config.ConfigApi])

  return frontend, api


frontend_app, endpoints_app = create_applications()
