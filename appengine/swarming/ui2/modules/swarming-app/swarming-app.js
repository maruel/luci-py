// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

/** @module swarming-ui/modules/swarming-app
 * @description <h2><code>swarming-app</code></h2>
 * <p>
 *   A general application layout which includes a responsive
 *   side panel. This element is largely CSS, with a smattering of
 *   JS to toggle the side panel on/off when in small screen mode.
 *   A notable addition to the top panel is an &lt;oauth-login&gt; element
 *   to handle login. See the demo page for an example usage.
 * </p>
 *
 * <p>
 *   The swarming-app can be a central place for indicating to the user
 *   that the app is busy (e.g. RPCs). Simply use the addBusyTasks()
 *   and finishedTask() to indicate when work is starting and stopping.
 *   The 'busy-end' event will signal any time a finishedTask() drops the
 *   count of ongoing tasks to zero (or lower). See also the busy property.
 * </p>
 *
 * @evt busy-end This event is emitted whenever the app transitions from
 *               busy to not busy.
 *
 * @attr client_id - The Client ID for authenticating via OAuth.
 * @attr testing_offline - If true, the real OAuth flow won't be used.
 *    Instead, dummy data will be used. Ideal for local testing.
 *
 */

import { errorMessage } from 'elements-sk/errorMessage'
import { html, render } from 'lit-html'
import { jsonOrThrow } from 'common-sk/modules/jsonOrThrow'
import { upgradeProperty } from 'elements-sk/upgradeProperty'

import 'elements-sk/icon/menu-icon-sk'
import 'elements-sk/spinner-sk'

import '../oauth-login'

const button_template = document.createElement('template');
button_template.innerHTML =`
<button class=toggle-button>
  <menu-icon-sk>
  </menu-icon-sk>
</button>
`;

const spinner_template = document.createElement('template');
spinner_template.innerHTML =`
<div class=spinner-spacer>
  <spinner-sk></spinner-sk>
</div>
`;

function versionLink(details) {
  if (!details || !details.server_version) {
    return '#';
  }
  var split = details.server_version.split('-');
  if (split.length !== 2) {
    return '#';
  }
  return `https://chromium.googlesource.com/infra/luci/luci-py/+/${split[1]}`;
}

const dynamic_content_template = (ele) => html`
<div class=server-version>
  Server:
  <a href=${versionLink(ele._server_details)}>
    ${ele._server_details.server_version}
  </a>
</div>
<oauth-login client_id=${ele.client_id}
             ?testing_offline=${ele.testing_offline}>
</oauth-login>
`;

window.customElements.define('swarming-app', class extends HTMLElement {

  constructor() {
    super();
    this._busyTaskCount = 0;
    this._spinner = null;
    this._dynamicEle = null;
    this._auth_header = '';
    this._server_details = {
      server_version: 'You must log in to see more details',
      bot_version: '',
    };
    this._permissions = {};
  }

  connectedCallback() {
    upgradeProperty(this, 'client_id');
    upgradeProperty(this, 'testing_offline');
    this._addHTML();

    this.addEventListener('log-in', (e) => {
      this._auth_header = e.detail.auth_header;
      this._fetch();
    });

    this._render();
  }

  static get observedAttributes() {
    return ['client_id', 'testing_offline'];
  }


  /** @prop {boolean} busy Indicates if there any on-going tasks (e.g. RPCs).
   *                  This also mirrors the status of the embedded spinner-sk.
   *                  Read-only. */
  get busy() { return !!this._busyTaskCount;}

  /** @prop {Object} permissions The permissions the server says the logged-in
                     user has. This is empty object if user is not logged in.
   *                 Read-only. */
  get permissions() { return this._permissions; }

  /** @prop {Object} server_details The details about the server or a
                     placeholder object if the user is not logged in or
   *                 not authorized. Read-only. */
  get server_details() { return this._server_details; }


  /** @prop {string} client_id Mirrors the attribute 'client_id'. */
  get client_id() { return this.getAttribute('client_id');}
  set client_id(val) { return this.setAttribute('client_id', val);}

  /** @prop {bool} testing_offline Mirrors the attribute 'testing_offline'. */
  get testing_offline() { return this.hasAttribute('testing_offline');}
  set testing_offline(val) {
    if (val) {
      this.setAttribute('testing_offline', true);
    } else {
      this.removeAttribute('testing_offline');
    }
  }

  /**
   * Indicate there are some number of tasks (e.g. RPCs) the app is waiting on
   * and should be in the "busy" state, if it isn't already.
   *
   * @param {Number} count - Number of tasks to wait for. Should be positive.
   */
  addBusyTasks(count) {
    this._busyTaskCount += count;
    if (this._spinner && this._busyTaskCount > 0) {
      this._spinner.active = true;
    }
  }

  /**
   * Removes one task from the busy count. If there are no more tasks to wait
   * for, the app will leave the "busy" state and emit the "busy-end" event.
   *
   */
  finishedTask() {
    this._busyTaskCount--;
    if (this._busyTaskCount <= 0) {
      this._busyTaskCount = 0;
      if (this._spinner) {
        this._spinner.active = false;
      }
      this.dispatchEvent(new CustomEvent('busy-end', {bubbles: true}));
    }
  }

  /**
   * As mentioned in the element description, the main point of this element
   * is to insert a little bit of CSS and a few HTML elements for consistent
   * theming and functionality.
   *
   * This function adds in the following:
   * <ol>
   *   <li> A button that will toggle the side panel on small screens (and will
   *      be hidden on large screens).</li>
   *   <li> The spinner that indicates the busy state.</li>
   *   <li> A spacer span to right-align the following elements.</li>
   *   <li> A placeholder in which to render information about the server.</li>
   *   <li> A placeholder in which to render the login-element.</li>
   * </ol>
   *
   * This function need only be called once, when the element is created.
   */
  _addHTML() {
    let header = this.querySelector('header');
    let sidebar = header && header.querySelector('aside');
    if (!(header && sidebar && sidebar.classList.contains('hideable'))) {
      return;
    }
    // Add the collapse button to the header as the first item.
    let btn = button_template.content.cloneNode(true);
    // btn is a document-fragment, so we need to insert it into the
    // DOM to make it "expand" into a real button. Then, and only then,
    // we can add a "click" listener.
    header.insertBefore(btn, header.firstElementChild);
    btn = header.firstElementChild;
    btn.addEventListener('click', (e) => this._toggleMenu(e, sidebar));

    // Add the spinner that will visually indicate the state of the
    // busy property.
    let spinner = spinner_template.content.cloneNode(true);
    header.insertBefore(spinner, sidebar);
    // The real spinner is a child of the template, so we need to grab it
    // from the header after the template has been expanded.
    this._spinner = header.querySelector('spinner-sk');

    let spacer = document.createElement('span');
    spacer.classList.add('grow');
    header.appendChild(spacer);

    // The placeholder for which the server details and login element (the only
    // dynamic content swarming-app manages) will be rendered into. See
    // _render() for when that happens.
    this._dynamicEle = document.createElement('div');
    this._dynamicEle.classList.add('right');
    header.appendChild(this._dynamicEle);
  }

  _toggleMenu(e, sidebar) {
    sidebar.classList.toggle('shown');
  }

  _fetch() {
    if (!this._auth_header) {
      return;
    }
    this._server_details = {
      server_version: '<loading>',
      bot_version: '<loading>',
    };
    let auth = {
      headers: {'authorization': this._auth_header}
    };
    this.addBusyTasks(2);
    fetch('/_ah/api/swarming/v1/server/details', auth)
      .then(jsonOrThrow)
      .then((json) => {
        this._server_details = json;
        this._render();
        this.dispatchEvent(new CustomEvent('server-details-loaded',
                                           {bubbles: true}));
        this.finishedTask();
      })
      .catch((e) => {
        if (e.status === 403) {
          this._server_details = {
            server_version: 'User unauthorized - try logging in ' +
                            'with a different account',
            bot_version: '',
          };
          this._render();
        } else {
          console.error(e);
          errorMessage(`Unexpected error loading details: ${e.message}`, 5000);
        }
        this.finishedTask();
      });
    fetch('/_ah/api/swarming/v1/server/permissions', auth)
      .then(jsonOrThrow)
      .then((json) => {
        this._permissions = json;
        this._render();
        this.dispatchEvent(new CustomEvent('permissions-loaded',
                                           {bubbles: true}));
        this.finishedTask();
      })
      .catch((e) => {
        if (e.status !== 403) {
          console.error(e);
          errorMessage(`Unexpected error loading permissions: ${e.message}`,
                       5000);
        }
        this.finishedTask();
      });
  }

  _render() {
    if (this._dynamicEle) {
      render(dynamic_content_template(this), this._dynamicEle);
    }

  }

  attributeChangedCallback(attrName, oldVal, newVal) {
    this._render();
  }

});
