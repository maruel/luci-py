// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

/** @module swarming-ui/test_util
 * @description
 *
 * <p>
 *  A general set of useful functions for tests and demos, e.g. reducing boilerplate.
 * </p>
 */

export function mockAppGETs(fetchMock, permissions) {
  fetchMock.get('/_ah/api/swarming/v1/server/details', {
    server_version: '1234-abcdefg',
    bot_version: 'abcdoeraymeyouandme',
  });


  fetchMock.get('/_ah/api/swarming/v1/server/permissions', permissions);
}

export function mockAuthdAppGETs(fetchMock, permissions) {
  fetchMock.get('/_ah/api/swarming/v1/server/details', requireLogin({
    server_version: '1234-abcdefg',
    bot_version: 'abcdoeraymeyouandme',
  }));


  fetchMock.get('/_ah/api/swarming/v1/server/permissions', requireLogin(permissions));
}

export function requireLogin(logged_in, delay=500) {
  return function(url, opts){
    if (opts && opts.headers && opts.headers.authorization) {
      return new Promise((resolve) => {
        setTimeout(resolve, delay);
      }).then(() => {
        return {
          status: 200,
          body: JSON.stringify(logged_in),
          headers: {'Content-Type':'application/json'},
        };
      });
    } else {
      return new Promise((resolve) => {
        setTimeout(resolve, delay);
      }).then(() => {
        return {
          status: 403,
          body: 'Try logging in',
          headers: {'Content-Type':'text/plain'},
        };
      });
    }
  };
}