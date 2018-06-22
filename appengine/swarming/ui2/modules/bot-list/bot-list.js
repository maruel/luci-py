// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

/** @module swarming-ui/modules/bot-list
 * @description <h2><code>bot-list</code></h2>
 *
 * <p>
 *  Bot List shows a filterable list of all bots in the fleet.
 * </p>
 *
 * <p>This is a top-level element.</p>
 *
 * @attr client_id - The Client ID for authenticating via OAuth.
 * @attr testing_offline - If true, the real OAuth flow won't be used.
 *    Instead, dummy data will be used. Ideal for local testing.
 *
 */

import { html, render } from 'lit-html/lib/lit-extended'
import { jsonOrThrow } from 'common-sk/modules/jsonOrThrow'
import naturalSort from 'javascript-natural-sort/naturalSort'

import 'common-sk/modules/select-sk'
import 'elements-sk/checkbox-sk'
import 'elements-sk/icon/arrow-forward-icon-sk'
import 'elements-sk/icon/remove-circle-outline-icon-sk'

import { stableSort } from '../util'
import { aggregateTemps, attribute, botLink, column, colHeaderMap,
         devices, extraKeys, fromDimension, fromState, longestOrAll, processBots,
         processDimensions, processPrimaryMap, specialSortMap, taskLink } from './bot-list-helpers'
import SwarmingAppBoilerplate from '../SwarmingAppBoilerplate'

const colHead = (col, ele) => html`
<th>${colHeaderMap[col] || col}
  <sort-toggle key=${col} current=${ele._sort} direction=${ele._dir}></sort-toggle>
</th>
`;

const botCol = (col, bot, ele) => html`
<td>${column(col, bot, ele)}</td>
`;

const botRow = (bot, ele) => html`
<tr class$="bot-row ${ele._botClass(bot)}">${ele._cols.map((col) => botCol(col,bot,ele))}</tr>
`;

const primaryOption = (key, ele) => html`
<div class="item" selected?=${ele._primaryKey === key}>
  <span>${key}</span>
  <span class=flex></span>
  <checkbox-sk checked?=${ele._cols.indexOf(key) !== -1}></checkbox-sk>
</div>
`

const secondaryOptions = (ele) => {
  let values = ele._primaryMap[ele._primaryKey];
  if (!values) {
    return html`<div class="information_only">Only dimensions can be used for filtering.
<i>${ele._primaryKey}</i> is a part of the bot's state and is informational only.</div>`
  }
  return values.map((value) =>
  html`<div class="item">
  <span>${value}</span>
  <span class=flex></span>
  <arrow-forward-icon-sk></arrow-forward-icon-sk>
</div>`)
}


const filterOption = (value, ele) => html`
<div class="item">
  <span>${value}</span>
  <span class=flex></span>
  <remove-circle-outline-icon-sk></remove-circle-outline-icon-sk>
</div>
`

// can't use <select> and <option> because <option> strips out non-text (e.g. checkboxes)
const filters = (ele) => html`
<!-- primary key selector-->
<select-sk class=selector on-selection-changed=${(e) => ele._primayKeyChanged(e)}>
  ${ele._primaryArr.map((key) => primaryOption(key, ele))}
</select-sk>
<!-- secondary value selector-->
<select-sk class=selector>
  ${secondaryOptions(ele)}
</select-sk>
<!-- filters selector-->
<select-sk class=selector>
  ${ele._filters.map((filter) => filterOption(filter, ele))}
</select-sk>
`

const template = (ele) => html`
<swarming-app id=swapp
              client_id=${ele.client_id}
              testing_offline=${ele.testing_offline}>
  <header>
    <div class=title>Swarming Server</div>
      <aside class=hideable>
        <a href=/>Home</a>
        <a href=/botlist>Bot List</a>
        <a href=/tasklist>Task List</a>
      </aside>
  </header>
  <main>
    <h2 class=message hidden?=${ele.loggedInAndAuthorized}>${ele._message}</h2>

    ${filters(ele)}

    <table class=bot-table hidden?=${!ele.loggedInAndAuthorized}>
      <thead><tr>${ele._cols.map((col) => colHead(col,ele))}</tr></thead>
      <tbody>${ele._sortBots().map((bot) => botRow(bot,ele))}</tbody>
    </table>
  </main>
  <footer><error-toast-sk></error-toast-sk></footer>
</swarming-app>`;

window.customElements.define('bot-list', class extends SwarmingAppBoilerplate {

  constructor() {
    super(template);
    this._bots = [];
    // TODO(kjlubick): pull these from url params
    this._cols = ['id', 'task', 'os', 'status'];
    this._filters = ['pool:Skia', 'likesDogs:yes'];
    this._primaryKey = 'os'


    /** _primaryArr: Array<String>, the display order of the primary keys.
        This is dimensions, then bot properties, then elements from bot.state. */
    this._primaryArr = [];
    /** _primaryMap: Object, a mapping of primary keys to secondary items.
        The primary keys are things that can be columns or sorted by.  The
        primary values (aka the secondary items) are things that can be filtered
        on. Primary consists of dimensions and state.  Secondary contains the
        values primary things can be.*/
    this._primaryMap = {
      'os': ['Windows', 'Linux', 'Android', 'Gerber'],
      'id': [],
      'gpu': ['Nvidia', 'Intel', 'RaspberryPi']
    };
    this._dimensions = [];


    this._limit = 100;
    this._sort = 'id';
    this._dir = 'asc';
    this._verbose = false;
    this._message = 'You must sign in to see anything useful.';
  }

  connectedCallback() {
    super.connectedCallback();

    this.addEventListener('log-in', (e) => {
      this._update();
      this.render();
    });

    this.addEventListener('sort-change', (e) => {
      this._sort = e.detail.key;
      this._dir = e.detail.direction;
      this.render();
    });

    this.render();
  }

  _botClass(bot) {
    let classes = '';
    if (bot.is_dead) {
      classes += 'dead ';
    }
    if (bot.quarantined) {
      classes += 'quarantined ';
    }
    if (bot.maintenance_msg) {
      classes += 'maintenance ';
    }
    if (bot.version !== this.server_details.server_version) {
      classes += 'old_version';
    }
    return classes;
  }

  _primayKeyChanged(e) {
    this._primaryKey = this._primaryArr[e.detail.selection];
    this.render();
  }

  /* sort the internal set of bots based on the sort-toggle and direction
   * and returns it (for use in templating) */
  _sortBots() {
    console.time('_sortBots');
    stableSort(this._bots, (botA, botB) => {
      let sortOn = this._sort;
      if (!sortOn) {
        return 0;
      }
      let dir = 1;
      if (this._dir === 'desc') {
        dir = -1;
      }
      let sorter = specialSortMap[sortOn];
      if (sorter) {
        return sorter(dir, botA, botB);
      }
      // Default to a natural compare of the columns.
      let aCol = column(sortOn, botA, this);
      if (aCol === 'none'){
        // put "none" at the bottom of the sort order
        aCol = 'ZZZ';
      }
      var bCol = column(sortOn, botB, this);
      if (bCol === 'none'){
        // put "none" at the bottom of the sort order
        bCol = 'ZZZ';
      }
      return dir * naturalSort(aCol, bCol);
    });
    console.timeEnd('_sortBots');
    return this._bots;
  }

  _update() {
    if (!this.loggedInAndAuthorized) {
      return;
    }
    let extra = {
      headers: {'authorization': this.auth_header}
    };
    let app = this.firstElementChild;
    app.addBusyTasks(2);
    // TODO(kjlubick): need query params
    fetch('/_ah/api/swarming/v1/bots/list', extra)
      .then(jsonOrThrow)
      .then((json) => {
        this._bots = processBots(json.items);
        this.render();
        app.finishedTask();
      })
      .catch((e) => this.fetchError(e, 'bots/list'));
    fetch('/_ah/api/swarming/v1/bots/dimensions', extra)
      .then(jsonOrThrow)
      .then((json) => {
        this._dimensions = processDimensions(json.bots_dimensions);
        this._primaryMap = processPrimaryMap(json.bots_dimensions);
        this._primaryArr = this._dimensions.concat(extraKeys);
        this.render();
        app.finishedTask();
      })
      .catch((e) => this.fetchError(e, 'bots/dimensions'));
  }

});
