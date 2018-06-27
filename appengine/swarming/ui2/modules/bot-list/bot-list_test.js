// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

import 'modules/bot-list'
import { deepCopy } from 'common-sk/modules/object'
import { $, $$ } from 'common-sk/modules/dom'

import { data_s10, fleetDimensions } from   'modules/bot-list/test_data'
import { colHeaderMap, column, processBots, processDimensions, processPrimaryMap } from 'modules/bot-list/bot-list-helpers'

if (!mockAppGETs) {
  var mockAppGETs = require('modules/test_util').mockAppGETs;
}

describe('bot-list', function() {
  const fetchMock = require('fetch-mock');

  beforeEach(function(){
    fetchMock.sandbox();

    // These are the default responses to the expected API calls (aka 'matched').
    // They can be overridden for specific tests, if needed.
    mockAppGETs(fetchMock, {
      delete_bot: true
    });

    // TODO(kjlubick): This will need to be a regex at some point
    fetchMock.get('/_ah/api/swarming/v1/bots/list', data_s10);

    fetchMock.get('/_ah/api/swarming/v1/bots/dimensions', fleetDimensions);

    // Everything else
    fetchMock.catch(404);
  });

  afterEach(function() {
    // Completely remove the mocking which allows each test
    // to be able to mess with the mocked routes w/o impacting other tests.
    fetchMock.restore();
  });

  // A reusable HTML element in which we create our element under test.
  let container = document.createElement('div');
  document.body.appendChild(container);

  afterEach(function() {
    container.innerHTML = '';
  });

  beforeEach(function() {
    // Fix the time so all of our relative dates work.
    jasmine.clock().install();
    jasmine.clock().mockDate(new Date(Date.UTC(2018, 5, 14, 12, 46, 22, 1234)));
  });

  afterEach(function() {
    jasmine.clock().uninstall();
  })

  // calls the test callback with one element 'ele', a created <swarming-index>.
  // We can't put the describes inside the whenDefined callback because
  // that doesn't work on Firefox (and possibly other places).
  function createElement(test) {
    return window.customElements.whenDefined('bot-list').then(() => {
      container.innerHTML = `<bot-list client_id=for_test testing_offline=true></bot-list>`;
      expect(container.firstElementChild).toBeTruthy();
      test(container.firstElementChild);
    });
  }

  function userLogsIn(ele, callback) {
    // The swarming-app emits the 'busy-end' event when all pending
    // fetches (and renders) have resolved.
    ele.addEventListener('busy-end', (e) => {
      callback();
    });
    let login = ele.querySelector('oauth-login');
    login._logIn();
    fetchMock.flush();
  }

  // convenience function to save indentation and boilerplate.
  // expects a function test that should be called with the created
  // <bot-list> after the user has logged in.
  function loggedInBotlist(test) {
    createElement((ele) => {
      userLogsIn(ele, () => {
        test(ele);
      });
    });
  }

//===============TESTS START====================================

  describe('html structure', function() {
    it('contains swarming-app as its only child', function(done) {
      createElement((ele) => {
        expect(ele.children.length).toBe(1);
        expect(ele.children[0].tagName).toBe('swarming-app'.toUpperCase());
        done();
      });
    });

    describe('when not logged in', function() {
      it('tells the user they should log in', function(done) {
        createElement((ele) => {
          let loginMessage = ele.querySelector('swarming-app>main .message');
          expect(loginMessage).toBeTruthy();
          expect(loginMessage.hidden).toBeFalsy('Message should not be hidden');
          expect(loginMessage.innerText).toContain('must sign in');
          done();
        })
      })
      it('does not display filters or bots', function(done) {
        createElement((ele) => {
          let botTable = ele.querySelector('.bot-table');
          expect(botTable).toBeTruthy();
          expect(botTable.hidden).toBeTruthy('.bot-table should be hidden');
          done();
        })
      });
    }); //end describe('when not logged in')

    describe('when logged in as unauthorized user', function() {

      function notAuthorized() {
        // overwrite the default fetchMock behaviors to have everything return 403.
        fetchMock.get('/_ah/api/swarming/v1/server/details', 403,
                      { overwriteRoutes: true });
        fetchMock.get('/_ah/api/swarming/v1/server/permissions', {},
                      { overwriteRoutes: true });
        fetchMock.get('/_ah/api/swarming/v1/bots/list', 403,
                      { overwriteRoutes: true });
      }

      beforeEach(notAuthorized);

      it('tells the user they should change accounts', function(done) {
        loggedInBotlist((ele) => {
          let loginMessage = ele.querySelector('swarming-app>main .message');
          expect(loginMessage).toBeTruthy();
          expect(loginMessage.hidden).toBeFalsy('Message should not be hidden');
          expect(loginMessage.innerText).toContain('different account');
          done();
        });
      });
      it('does not display filters or bots', function(done) {
        loggedInBotlist((ele) => {
          let botTable = ele.querySelector('.bot-table');
          expect(botTable).toBeTruthy();
          expect(botTable.hidden).toBeTruthy('.bot-table should be hidden');
          done();
        });
      });
    }); // end describe('when logged in as unauthorized user')

    describe('when logged in as user (not admin)', function() {

      describe('default landing page', function() {
        it('displays whatever bots show up', function(done) {
          loggedInBotlist((ele) => {
            let botRows = ele.querySelectorAll('.bot-table .bot-row');
            expect(botRows).toBeTruthy();
            expect(botRows.length).toBe(10, '(num botRows)');
            done();
          });
        });

        it('shows the default set of columns', function(done) {
          loggedInBotlist((ele) => {
            // ensure sorting is deterministic.
            ele._sort = 'id';
            ele._dir = 'asc';
            ele._verbose = false;
            ele.render();

            let colHeaders = ele.querySelectorAll('.bot-table thead th');
            expect(colHeaders).toBeTruthy();
            expect(colHeaders.length).toBe(4, '(num colHeaders)');

            expect(colHeaders[0].innerText.trim()).toBe('Bot Id');
            expect(colHeaders[1].innerText.trim()).toBe('Current Task');
            expect(colHeaders[2].innerText.trim()).toBe('OS');
            expect(colHeaders[3].innerText.trim()).toBe('Status');

            let rows = ele.querySelectorAll('.bot-table .bot-row');
            expect(rows).toBeTruthy();
            expect(rows.length).toBe(10, '10 rows');

            let cols = ele.querySelectorAll('.bot-table .bot-row td');
            expect(cols).toBeTruthy();
            expect(cols.length).toBe(4 * 10, '4 columns * 10 rows');
            // little helper for readability
            let cell = (r, c) => cols[4*r+c];

            // Check the content of the first few rows (after sorting)
            expect(rows[0]).not.toHaveClass('dead');
            expect(rows[0]).not.toHaveClass('quarantined');
            expect(rows[0]).not.toHaveClass('old_version');
            expect(cell(0, 0).innerText).toBe('somebot10-a9');
            expect(cell(0, 0).innerHTML).toContain('<a ', 'has a link');
            expect(cell(0, 0).innerHTML).toContain('href="/bot?id=somebot10-a9"', 'link is correct');
            expect(cell(0, 1).innerText).toBe('idle');
            expect(cell(0, 1).innerHTML).not.toContain('<a ', 'no link');
            expect(cell(0, 2).innerText).toBe('Ubuntu-17.04');
            expect(cell(0, 3).innerText).toContain('Alive');

            expect(rows[1]).toHaveClass('quarantined');
            expect(cell(1, 0).innerText).toBe('somebot11-a9');
            expect(cell(1, 1).innerText).toBe('idle');
            expect(cell(1, 2).innerText).toBe('Android');
            expect(cell(1, 3).innerText).toContain('Quarantined');
            expect(cell(1, 3).innerText).toContain('[too_hot,low_battery]');

            expect(rows[2]).toHaveClass('dead');
            expect(rows[2]).toHaveClass('old_version');
            expect(cell(2, 0).innerText).toBe('somebot12-a9');
            expect(cell(2, 1).innerText).toBe('3e17182091d7ae11');
            expect(cell(2, 1).innerHTML).toContain('<a ', 'has a link');
            expect(cell(2, 1).innerHTML).toContain('href="/task?id=3e17182091d7ae10"',
                                      'link is pointing to the cannonical (0 ending) page');
            expect(cell(2, 1).innerHTML).toContain('title="Perf-Win10-Clang-Golo',
                                      'Mouseover with task name');
            expect(cell(2, 2).innerText).toBe('Windows-10-16299.431');
            expect(cell(2, 3).innerText).toContain('Dead');
            expect(cell(2, 3).innerText).toContain('Last seen 1w ago');

            expect(rows[3]).toHaveClass('maintenance');
            expect(cell(3, 3).innerText).toContain('Maintenance');
            expect(cell(3, 3).innerText).toContain('Need to re-format the hard drive.');

            expect(rows[4]).toHaveClass('old_version');
            done();
          });
        });

        it('updates the sort-toggles based on the current sort direction', function(done) {
          loggedInBotlist((ele) => {
            ele._sort = 'id';
            ele._dir = 'asc';
            ele.render();

            let sortToggles = ele.querySelectorAll('.bot-table thead sort-toggle');
            expect(sortToggles).toBeTruthy();
            expect(sortToggles.length).toBe(4, '(num sort-toggles)');

            expect(sortToggles[0].key).toBe('id');
            expect(sortToggles[0].current).toBe('id');
            expect(sortToggles[0].direction).toBe('asc');
            // spot check one of the other ones
            expect(sortToggles[2].key).toBe('os');
            expect(sortToggles[2].current).toBe('id');
            expect(sortToggles[2].direction).toBe('asc');

            ele._sort = 'task';
            ele._dir = 'desc';
            ele.render();

            expect(sortToggles[0].key).toBe('id');
            expect(sortToggles[0].current).toBe('task');
            expect(sortToggles[0].direction).toBe('desc');

            expect(sortToggles[1].key).toBe('task');
            expect(sortToggles[1].current).toBe('task');
            expect(sortToggles[1].direction).toBe('desc');
            done();
          });
        });
      }); // end describe('default landing page')

    });// end describe('when logged in as user')

  }); // end describe('html structure')

  describe('dynamic behavior', function() {
    // This is done w/o interacting with the sort-toggles because that is more
    // complicated with adding the event listener and so on.
    it('can stable sort in ascending order', function(done){
      loggedInBotlist((ele) => {
        ele._verbose = false;
        // First sort in descending id order
        ele._sort = 'id';
        ele._dir = 'desc';
        ele.render();
        // next sort in ascending os order
        ele._sort = 'os';
        ele._dir = 'asc';
        ele.render();

        let actualOSOrder = ele._bots.map((b) => column('os', b, ele));
        let actualIDOrder = ele._bots.map((b) => b.bot_id);

        expect(actualOSOrder).toEqual(['Android', 'Ubuntu-17.04', 'Ubuntu-17.04', 'Ubuntu-17.04',
          'Ubuntu-17.04', 'Ubuntu-17.04', 'Windows-10-16299.309', 'Windows-10-16299.309',
          'Windows-10-16299.431', 'Windows-10-16299.431']);
        expect(actualIDOrder).toEqual([
          'somebot11-a9', // Android
          'somebot77-a3', 'somebot15-a9', 'somebot13-a9', 'somebot13-a2', 'somebot10-a9', // Ubuntu in descending id
          'somebot17-a9', 'somebot16-a9',   // Win10.309
          'somebot18-a9', 'somebot12-a9']); // Win10.431
        done();
      });
    });

    it('can stable sort in descending order', function(done){
      loggedInBotlist((ele) => {
        ele._verbose = false;
        // First sort in asc id order
        ele._sort = 'id';
        ele._dir = 'asc';
        ele.render();
        // next sort in descending os order
        ele._sort = 'os';
        ele._dir = 'desc';
        ele.render();

        let actualOSOrder = ele._bots.map((b) => column('os', b, ele));
        let actualIDOrder = ele._bots.map((b) => b.bot_id);

        expect(actualOSOrder).toEqual(['Windows-10-16299.431', 'Windows-10-16299.431',
          'Windows-10-16299.309', 'Windows-10-16299.309', 'Ubuntu-17.04', 'Ubuntu-17.04',
          'Ubuntu-17.04', 'Ubuntu-17.04', 'Ubuntu-17.04', 'Android']);
        expect(actualIDOrder).toEqual([
          'somebot12-a9', 'somebot18-a9', // Win10.431
          'somebot16-a9', 'somebot17-a9', // Win10.309
          'somebot10-a9', 'somebot13-a2', 'somebot13-a9', 'somebot15-a9', 'somebot77-a3',  // Ubuntu in ascending id
          'somebot11-a9']); // Android
        done();
      });
    });

    it('toggles columns by clicking on the boxes in the "key selector"', function(done) {
      loggedInBotlist((ele) => {
        ele._cols = ['id', 'task', 'os', 'status'];
        ele.render();

        let keySelector = ele.querySelector('.selector.keys');
        expect(keySelector).toBeTruthy();

        // click on first non checked checkbox.
        let keyToClick = null;
        let checkbox = null;
        for (let i = 0; i < keySelector.children.length; i++) {
          let child = keySelector.children[i];
          checkbox = child.querySelector('checkbox-sk');
          keyToClick = child.querySelector('.key');
          expect(keyToClick).toBeTruthy();
          if (!checkbox.checked) {
            keyToClick = keyToClick.textContent;
            break;
          }
        }
        checkbox.click(); // click is synchronous, it returns after
                          // the clickHandler is run.
        // Check underlying data
        expect(ele._cols).toContain(keyToClick);
        // check the rendering changed
        let colHeaders = $('.bot-table thead th');
        expect(colHeaders).toBeTruthy();
        expect(colHeaders.length).toBe(5, '(num colHeaders)');
        let expectedHeader = colHeaderMap[keyToClick] || keyToClick;
        expect(colHeaders.map((c) => c.textContent.trim())).toContain(expectedHeader);

        // click it again
        checkbox.click();

        // Check underlying data
        expect(ele._cols).not.toContain(keyToClick);
        // check the rendering changed
        colHeaders = $('.bot-table thead th');
        expect(colHeaders).toBeTruthy();
        expect(colHeaders.length).toBe(4, '(num colHeaders)');
        expectedHeader = colHeaderMap[keyToClick] || keyToClick;
        expect(colHeaders.map((c) => c.textContent.trim())).not.toContain(expectedHeader);
        done();
      });
    });

    function getKeySelectorRow(ele, key) {
      let keySelector = ele.querySelector('.selector.keys');
      expect(keySelector).toBeTruthy();

      for (let i = 0; i < keySelector.children.length; i++) {
        let child = keySelector.children[i];
        let keyToClick = child.querySelector('.key');
        expect(keyToClick).toBeTruthy();
        if (keyToClick.textContent.trim() === key) {
          return child;
        }
      }
      fail(`Could not find keySelectorRow with key ${key}`);
    }

    it('does not toggle forced columns (like "id")', function(done) {
      loggedInBotlist((ele) => {
        ele._cols = ['id', 'task', 'os', 'status'];
        ele.render();

        let row = getKeySelectorRow(ele, 'id');
        let checkbox = row.querySelector('checkbox-sk');
        expect(checkbox.checked).toBeTruthy();
        checkbox.click(); // click is synchronous, it returns after
                          // the clickHandler is run.
        // Check underlying data
        expect(ele._cols).toContain('id');
        // check there are still headers.
        let colHeaders = $('.bot-table thead th');
        expect(colHeaders).toBeTruthy();
        expect(colHeaders.length).toBe(4, '(num colHeaders)');
        done();
      });
    });

    function childrenAsArray(ele) {
      return Array.prototype.slice.call(ele.children);
    }

    it('shows values when a key row is selected', function(done) {
      loggedInBotlist((ele) => {
        ele._cols = ['id', 'task', 'os', 'status'];
        ele.render();
        let row = getKeySelectorRow(ele, 'cpu');
        expect(row).toBeTruthy();
        row.click();
        expect(row.hasAttribute('selected')).toBeTruthy();
        expect(ele._primaryKey).toBe('cpu');

        let valueSelector = $$('.selector.values');
        expect(valueSelector).toBeTruthy();
        let values = childrenAsArray(valueSelector).map((c) => c.textContent.trim());
        // spot check
        expect(values.length).toBe(8);
        expect(values).toContain('arm-32');
        expect(values).toContain('x86-64');

        let oldRow = row;
        row = getKeySelectorRow(ele, 'device_os');
        expect(row).toBeTruthy();
        row.click();
        expect(row.hasAttribute('selected')).toBeTruthy('new row only one selected');
        expect(oldRow.hasAttribute('selected')).toBeFalsy('old row unselected');
        expect(ele._primaryKey).toBe('device_os');

        valueSelector = $$('.selector.values');
        expect(valueSelector).toBeTruthy();
        values = childrenAsArray(valueSelector).map((c) => c.textContent.trim());
        // spot check
        expect(values.length).toBe(19);
        expect(values).toContain('none');
        expect(values).toContain('LMY49K.LZC89');

        done();
      });
    });

    function getValueSelectorRow(ele, value) {
      let valueSelector = ele.querySelector('.selector.values');
      expect(valueSelector).toBeTruthy();

      for (let i = 0; i < valueSelector.children.length; i++) {
        let child = valueSelector.children[i];
        let valueToClick = child.querySelector('.value');
        expect(valueToClick).toBeTruthy('all rows should have a value');
        if (valueToClick.textContent.trim() === value) {
          return child;
        }
      }
      fail(`Could not find valueSelectorRow with value ${value}`);
    }

    it('adds a filter when the arrow clicked', function(done) {
      loggedInBotlist((ele) => {
        ele._cols = ['id', 'task', 'os', 'status'];
        ele._primaryKey = 'os';  // set 'os' selected
        ele._filters = [];  // no filters
        ele.render();

        let valueRow = getValueSelectorRow(ele, 'Android');
        let arrow = valueRow.querySelector('arrow-forward-icon-sk');
        expect(arrow).toBeTruthy('there should be an arrow');
        arrow.click();

        expect(ele._filters.length).toBe(1, 'a filter should be added');
        expect(ele._filters[0]).toEqual('os:Android');

        let filterSelector = ele.querySelector('.selector.filters');
        expect(filterSelector).toBeTruthy('there should be a filter selector');
        expect(filterSelector.children.length).toBe(1);
        expect(arrow.hasAttribute('hidden'))
              .toBeTruthy('arrow should go away after being clicked');
        done();
      });
    });

  }); // end describe('dynamic behavior')

  describe('api calls', function() {
    function expectNoUnmatchedCalls() {
      let calls = fetchMock.calls(false, 'GET');
      expect(calls.length).toBe(0, 'no unmatched GETs');
      calls = fetchMock.calls(false, 'POST');
      expect(calls.length).toBe(0, 'no unmatched POSTs');
    }

    it('makes no API calls when not logged in', function(done) {
      createElement((ele) => {
        fetchMock.flush().then(() => {
          // true in the first argument means 'matched calls',
          // that is calls that we expect and specified in the
          // beforeEach at the top of this file.
          let calls = fetchMock.calls(true, 'GET');
          expect(calls.length).toBe(0);
          calls = fetchMock.calls(true, 'POST');
          expect(calls.length).toBe(0);

          expectNoUnmatchedCalls();
          done();
        });
      });
    });

    it('makes auth\'d API calls when a logged in user views landing page', function(done) {
      loggedInBotlist((ele) => {
        let calls = fetchMock.calls(true, 'GET');
        expect(calls.length).toBe(2+2, '2 GETs from swarming-app, 2 from bot-list');
        // calls is an array of 2-length arrays with the first element
        // being the string of the url and the second element being
        // the options that were passed in
        let gets = calls.map((c) => c[0]);
        // TODO(kjlubick): This may need to be a customMatcher or a partial match.
        expect(gets).toContain('/_ah/api/swarming/v1/bots/list');

        // check authorization headers are set
        calls.forEach((c) => {
          expect(c[1].headers).toBeDefined();
          expect(c[1].headers.authorization).toContain('Bearer ');
        })

        calls = fetchMock.calls(true, 'POST');
        expect(calls.length).toBe(0, 'no POSTs on bot-list');

        expectNoUnmatchedCalls();
        done();
      });
    });
  }); // end describe('api calls')

  describe('data parsing', function() {
    const LINUX_BOT = data_s10.items[0];
    const MULTI_ANDROID_BOT = data_s10.items[2];

    it('inflates the state', function() {
      // Make a copy of the object because _processBots will modify it in place.
      let bots = processBots([deepCopy(LINUX_BOT)]);
      expect(bots).toBeTruthy();
      expect(bots.length).toBe(1);
      expect(typeof bots[0].state).toBe('object');
    });

    it('makes a disk cache using the free space of disks', function() {
      // Make a copy of the object because _processBots will modify it in place.
      let bots = processBots([deepCopy(LINUX_BOT)]);
      let disks = bots[0].disks;
      expect(disks).toBeTruthy();
      expect(disks.length).toBe(2, 'Two disks');
      expect(disks[0]).toEqual({id: '/', mb: 680751.3}, 'biggest disk first');
      expect(disks[1]).toEqual({id: '/boot', mb: 842.2});
    });

    it('aggregates the temperatures of the host bot', function() {
      // Make a copy of the object because _processBots will modify it in place.
      let bots = processBots([deepCopy(LINUX_BOT)]);
      let temp = bots[0].state.temp;
      expect(temp).toBeTruthy();
      expect(temp.average).toBe('34.8', 'rounds to one decimal place');
      expect(temp.zones).toBe('thermal_zone0: 34.5 | thermal_zone1: 35', 'joins with |');
    });

    it('turns the device map into a list', function() {
      // Make a copy of the object because _processBots will modify it in place.
      let bots = processBots([deepCopy(MULTI_ANDROID_BOT)]);
      let devices = bots[0].state.devices;
      expect(devices).toBeTruthy();
      expect(devices.length).toBe(3, '3 devices attached to this bot');

      expect(devices[0].serial).toBe('3456789ABC', 'alphabetical by serial');
      expect(devices[0].okay).toBeTruthy();
      expect(devices[0].device_type).toBe('bullhead');
      expect(devices[0].temp.average).toBe('34.4');

      expect(devices[1].serial).toBe('89ABCDEF012', 'alphabetical by serial');
      expect(devices[1].okay).toBeFalsy();
      expect(devices[1].device_type).toBe('bullhead');
      expect(devices[1].temp.average).toBe('36.2');

      expect(devices[2].serial).toBe('Z01234567', 'alphabetical by serial');
      expect(devices[2].okay).toBeFalsy();
      expect(devices[2].device_type).toBe('bullhead');
      expect(devices[2].temp.average).toBe('34.3');
    });

    it('turns the dimension map into a list', function() {
      // processDimensions may modify the passed in variable.
      let dimensions = processDimensions(deepCopy(fleetDimensions.bots_dimensions));

      expect(dimensions).toBeTruthy();
      expect(dimensions.length).toBe(14);
      expect(dimensions).toContain('id');
      expect(dimensions).toContain('cores');
      expect(dimensions).toContain('device_type');
      expect(dimensions).toContain('xcode_version');
      expect(dimensions).not.toContain('error');
    });

    it('gracefully handles null data', function() {
      // processDimensions may modify the passed in variable.
      let dimensions = processDimensions(null);

      expect(dimensions).toBeTruthy();
      expect(dimensions.length).toBe(0);

      let bots = processBots(null);

      expect(bots).toBeTruthy();
      expect(bots.length).toBe(0);
    });

    it('extracts the key->value map', function() {
      // processDimensions may modify the passed in variable.
      let pMap = processPrimaryMap(deepCopy(fleetDimensions.bots_dimensions));

      expect(pMap).toBeTruthy();
      // Note this list doesn't include the blacklisted keys.
      let expectedKeys = ['android_devices', 'cores', 'cpu', 'device', 'device_os',
          'device_type', 'gpu', 'hidpi', 'machine_type', 'os', 'pool',
          'xcode_version', 'zone', 'id', 'disk_space', 'task', 'status', 'is_mp_bot'];
      let actualKeys = Object.keys(pMap);
      actualKeys.sort();
      expectedKeys.sort();
      expect(expectedKeys).toEqual(actualKeys);

      // Spot check a few values of the keys.
      let expected = ['0', '1', '2', '3', '4', '5', '6', '7'];
      let actual = pMap['android_devices'];
      actual.sort();
      expect(expected).toEqual(actual, 'android_devices');

      expected = ['0', '1'];
      actual = pMap['hidpi'];
      actual.sort();
      expect(expected).toEqual(actual, 'hidpi');

      // Spot check custom options
      expect(pMap['status']).toBeTruthy();
      expect(pMap['status']).toContain('alive');
      expect(pMap['is_mp_bot']).toBeTruthy();
      expect(pMap['is_mp_bot']).toContain('false');
      expect(pMap['id']).toEqual([]);
    });
  }); // end describe('data parsing')

});