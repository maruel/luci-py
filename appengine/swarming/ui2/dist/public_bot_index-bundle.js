!function(e){var t={};function n(s){if(t[s])return t[s].exports;var i=t[s]={i:s,l:!1,exports:{}};return e[s].call(i.exports,i,i.exports,n),i.l=!0,i.exports}n.m=e,n.c=t,n.d=function(e,t,s){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:s})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var s=Object.create(null);if(n.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)n.d(s,i,function(t){return e[t]}.bind(null,i));return s},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/newres/",n(n.s=8)}([function(e,t,n){"use strict";function s(e,t){if(e.hasOwnProperty(t)){let n=e[t];delete e[t],e[t]=n}}n.d(t,"a",function(){return s})},function(e,t,n){"use strict";const s=new Map;class i{constructor(e,t,n,s=x){this.strings=e,this.values=t,this.type=n,this.partCallback=s}getHTML(){const e=this.strings.length-1;let t="",n=!0;for(let s=0;s<e;s++){const e=this.strings[s];t+=e;const i=c(e);t+=(n=i>-1?i<e.length:n)?l:o}return t+this.strings[e]}getTemplateElement(){const e=document.createElement("template");return e.innerHTML=this.getHTML(),e}}function r(e,t,n=function(e){let t=s.get(e.type);void 0===t&&(t=new Map,s.set(e.type,t));let n=t.get(e.strings);return void 0===n&&(n=new _(e,e.getTemplateElement()),t.set(e.strings,n)),n}){const i=n(e);let r=t.__templateInstance;if(void 0!==r&&r.template===i&&r._partCallback===e.partCallback)return void r.update(e.values);r=new y(i,e.partCallback,n),t.__templateInstance=r;const o=r._clone();r.update(e.values),w(t,t.firstChild),t.appendChild(o)}const o=`{{lit-${String(Math.random()).slice(2)}}}`,l=`\x3c!--${o}--\x3e`,a=new RegExp(`${o}|${l}`),u=/[ \x09\x0a\x0c\x0d]([^\0-\x1F\x7F-\x9F \x09\x0a\x0c\x0d"'>=/]+)[ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*)$/;function c(e){const t=e.lastIndexOf(">");return e.indexOf("<",t+1)>-1?e.length:t}class h{constructor(e,t,n,s,i){this.type=e,this.index=t,this.name=n,this.rawName=s,this.strings=i}}const d=e=>-1!==e.index;class _{constructor(e,t){this.parts=[],this.element=t;const n=this.element.content,s=document.createTreeWalker(n,133,null,!1);let i=-1,r=0;const l=[];let c,d;for(;s.nextNode();){i++,c=d;const t=d=s.currentNode;if(1===t.nodeType){if(!t.hasAttributes())continue;const n=t.attributes;let s=0;for(let e=0;e<n.length;e++)n[e].value.indexOf(o)>=0&&s++;for(;s-- >0;){const s=e.strings[r],o=u.exec(s)[1],l=n.getNamedItem(o),c=l.value.split(a);this.parts.push(new h("attribute",i,l.name,o,c)),t.removeAttribute(l.name),r+=c.length-1}}else if(3===t.nodeType){const e=t.nodeValue;if(e.indexOf(o)<0)continue;const n=t.parentNode,s=e.split(a),u=s.length-1;r+=u;for(let e=0;e<u;e++)n.insertBefore(""===s[e]?document.createComment(""):document.createTextNode(s[e]),t),this.parts.push(new h("node",i++));n.insertBefore(""===s[u]?document.createComment(""):document.createTextNode(s[u]),t),l.push(t)}else if(8===t.nodeType&&t.nodeValue===o){const e=t.parentNode,n=t.previousSibling;null===n||n!==c||n.nodeType!==Node.TEXT_NODE?e.insertBefore(document.createComment(""),t):i--,this.parts.push(new h("node",i++)),l.push(t),null===t.nextSibling?e.insertBefore(document.createComment(""),t):i--,d=c,r++}}for(const e of l)e.parentNode.removeChild(e)}}const f=(e,t)=>p(t)?(t=t(e),g):null===t?void 0:t,p=e=>"function"==typeof e&&!0===e.__litDirective,g={},m=e=>null===e||!("object"==typeof e||"function"==typeof e);class b{constructor(e,t,n,s){this.instance=e,this.element=t,this.name=n,this.strings=s,this.size=s.length-1,this._previousValues=[]}_interpolate(e,t){const n=this.strings,s=n.length-1;let i="";for(let r=0;r<s;r++){i+=n[r];const s=f(this,e[t+r]);if(s&&s!==g&&(Array.isArray(s)||"string"!=typeof s&&s[Symbol.iterator]))for(const e of s)i+=e;else i+=s}return i+n[s]}_equalToPreviousValues(e,t){for(let n=t;n<t+this.size;n++)if(this._previousValues[n]!==e[n]||!m(e[n]))return!1;return!0}setValue(e,t){if(this._equalToPreviousValues(e,t))return;const n=this.strings;let s;2===n.length&&""===n[0]&&""===n[1]?(s=f(this,e[t]),Array.isArray(s)&&(s=s.join(""))):s=this._interpolate(e,t),s!==g&&this.element.setAttribute(this.name,s),this._previousValues=e}}class v{constructor(e,t,n){this.instance=e,this.startNode=t,this.endNode=n,this._previousValue=void 0}setValue(e){if((e=f(this,e))!==g)if(m(e)){if(e===this._previousValue)return;this._setText(e)}else e instanceof i?this._setTemplateResult(e):Array.isArray(e)||e[Symbol.iterator]?this._setIterable(e):e instanceof Node?this._setNode(e):void 0!==e.then?this._setPromise(e):this._setText(e)}_insert(e){this.endNode.parentNode.insertBefore(e,this.endNode)}_setNode(e){this._previousValue!==e&&(this.clear(),this._insert(e),this._previousValue=e)}_setText(e){const t=this.startNode.nextSibling;e=void 0===e?"":e,t===this.endNode.previousSibling&&t.nodeType===Node.TEXT_NODE?t.textContent=e:this._setNode(document.createTextNode(e)),this._previousValue=e}_setTemplateResult(e){const t=this.instance._getTemplate(e);let n;this._previousValue&&this._previousValue.template===t?n=this._previousValue:(n=new y(t,this.instance._partCallback,this.instance._getTemplate),this._setNode(n._clone()),this._previousValue=n),n.update(e.values)}_setIterable(e){Array.isArray(this._previousValue)||(this.clear(),this._previousValue=[]);const t=this._previousValue;let n=0;for(const s of e){let e=t[n];if(void 0===e){let s=this.startNode;n>0&&(s=t[n-1].endNode=document.createTextNode(""),this._insert(s)),e=new v(this.instance,s,this.endNode),t.push(e)}e.setValue(s),n++}if(0===n)this.clear(),this._previousValue=void 0;else if(n<t.length){const e=t[n-1];t.length=n,this.clear(e.endNode.previousSibling),e.endNode=this.endNode}}_setPromise(e){this._previousValue=e,e.then(t=>{this._previousValue===e&&this.setValue(t)})}clear(e=this.startNode){w(this.startNode.parentNode,e.nextSibling,this.endNode)}}const x=(e,t,n)=>{if("attribute"===t.type)return new b(e,n,t.name,t.strings);if("node"===t.type)return new v(e,n,n.nextSibling);throw new Error(`Unknown part type ${t.type}`)};class y{constructor(e,t,n){this._parts=[],this.template=e,this._partCallback=t,this._getTemplate=n}update(e){let t=0;for(const n of this._parts)n?void 0===n.size?(n.setValue(e[t]),t++):(n.setValue(e,t),t+=n.size):t++}_clone(){const e=this.template.element.content.cloneNode(!0),t=this.template.parts;if(t.length>0){const n=document.createTreeWalker(e,133,null,!1);let s=-1;for(let e=0;e<t.length;e++){const i=t[e],r=d(i);if(r)for(;s<i.index;)s++,n.nextNode();this._parts.push(r?this._partCallback(this,i,n.currentNode):void 0)}}return e}}const w=(e,t,n=null)=>{let s=t;for(;s!==n;){const t=s.nextSibling;e.removeChild(s),s=t}};n.d(t,"a",function(){return N}),n.d(t,"b",function(){return r});const N=(e,...t)=>new i(e,t,"html",T),T=(e,t,n)=>{if("attribute"===t.type){if("on-"===t.rawName.substr(0,3)){return new class{constructor(e,t,n){this.instance=e,this.element=t,this.eventName=n}setValue(e){const t=f(this,e);t!==this._listener&&(null==t?this.element.removeEventListener(this.eventName,this):null==this._listener&&this.element.addEventListener(this.eventName,this),this._listener=t)}handleEvent(e){"function"==typeof this._listener?this._listener.call(this.element,e):"function"==typeof this._listener.handleEvent&&this._listener.handleEvent(e)}}(e,n,t.rawName.slice(3))}const s=t.name.substr(t.name.length-1);if("$"===s){const s=t.name.slice(0,-1);return new b(e,n,s,t.strings)}if("?"===s){return new class extends b{setValue(e,t){const n=this.strings;if(2!==n.length||""!==n[0]||""!==n[1])throw new Error("boolean attributes can only contain a single expression");{const n=f(this,e[t]);if(n===g)return;n?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}}(e,n,t.name.slice(0,-1),t.strings)}return new class extends b{setValue(e,t){const n=this.strings;let s;this._equalToPreviousValues(e,t)||((s=2===n.length&&""===n[0]&&""===n[1]?f(this,e[t]):this._interpolate(e,t))!==g&&(this.element[this.name]=s),this._previousValues=e)}}(e,n,t.rawName,t.strings)}return x(e,t,n)}},function(e,t,n){"use strict";function s(e,t=1e4){"object"==typeof e&&(e=e.message||JSON.stringify(e));var n={message:e,duration:t};document.dispatchEvent(new CustomEvent("error-sk",{detail:n,bubbles:!0}))}n.d(t,"a",function(){return s})},function(e,t,n){"use strict";var s=n(1),i=n(0);n(15);const r=document.createElement("template");window.customElements.define("menu-icon-sk",class extends class extends HTMLElement{constructor(){super(),r.innerHTML=`<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">${this.constructor._svg}</svg>`}connectedCallback(){let e=r.content.cloneNode(!0);this.appendChild(e)}}{static get _svg(){return'<path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>'}}),window.customElements.define("spinner-sk",class extends HTMLElement{connectedCallback(){Object(i.a)(this,"active")}get active(){return this.hasAttribute("active")}set active(e){e?this.setAttribute("active",""):this.removeAttribute("active")}});n(13),n(12);var o=n(2);window.customElements.define("oauth-login",class extends HTMLElement{connectedCallback(){Object(i.a)(this,"client_id"),Object(i.a)(this,"testing_offline"),this._auth_header="",this.testing_offline?this._profile={email:"missing@chromium.org",imageURL:"http://storage.googleapis.com/gd-wagtail-prod-assets/original_images/logo_google_fonts_color_2x_web_64dp.png"}:(this._profile=null,document.addEventListener("oauth-lib-loaded",()=>{gapi.auth2.init({client_id:this.client_id}).then(()=>{this._maybeFireLoginEvent(),this._render()},e=>{console.error(e),Object(o.a)(`Error initializing oauth: ${JSON.stringify(e)}`,1e4)})})),this._render()}static get observedAttributes(){return["client_id","testing_offline"]}get auth_header(){return this._auth_header}get client_id(){return this.getAttribute("client_id")}set client_id(e){return this.setAttribute("client_id",e)}get testing_offline(){return this.getAttribute("testing_offline")}set testing_offline(e){e&&"false"!==e?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}_maybeFireLoginEvent(){let e=gapi.auth2.getAuthInstance().currentUser.get();if(e.isSignedIn()){let t=e.getBasicProfile();this._profile={email:t.getEmail(),imageURL:t.getImageUrl()};let n=e.getAuthResponse(!0),s=`${n.token_type} ${n.access_token}`;return this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:s},bubbles:!0})),this._auth_header=s,!0}return this._profile=null,this._auth_header="",!1}_logIn(){if(this.testing_offline)this._auth_header="Bearer 12345678910-boomshakalaka",this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:this._auth_header},bubbles:!0})),this._render();else{let e=gapi.auth2.getAuthInstance();e&&e.signIn({scope:"email",prompt:"select_account"}).then(()=>{this._maybeFireLoginEvent()||console.warn("login was not successful; maybe user canceled"),this._render()})}}_logOut(){if(this.testing_offline)this._auth_header="",this._render(),window.location.reload();else{let e=gapi.auth2.getAuthInstance();e&&e.signOut().then(()=>{this._auth_header="",this._profile=null,window.location.reload()})}}_render(){Object(s.b)((e=>e.auth_header?s["a"]` <div> <img class=center id=avatar src="${e._profile.imageURL}" width=30 height=30> <span class=center>${e._profile.email}</span> <span class=center>|</span> <a class=center on-click=${()=>e._logOut()} href="#">Sign out</a> </div>`:s["a"]` <div> <a on-click=${()=>e._logIn()} href="#">Sign in</a> </div>`)(this),this)}attributeChangedCallback(e,t,n){this._render()}});const l=document.createElement("template");l.innerHTML="\n<button class=toggle-button>\n  <menu-icon-sk>\n  </menu-icon-sk>\n</button>\n";const a=document.createElement("template");a.innerHTML="\n<div class=spinner-spacer>\n  <spinner-sk></spinner-sk>\n</div>\n";window.customElements.define("swarming-app",class extends HTMLElement{connectedCallback(){Object(i.a)(this,"client_id"),Object(i.a)(this,"testing_offline"),this._busyTaskCount=0,this._spinner=null,this._loginEle=null,this._addHTML(),this._render()}static get observedAttributes(){return["client_id","testing_offline"]}get busy(){return!!this._busyTaskCount}get client_id(){return this.getAttribute("client_id")}set client_id(e){return this.setAttribute("client_id",e)}get testing_offline(){return this.getAttribute("testing_offline")}set testing_offline(e){e&&"false"!==e?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}addBusyTasks(e){this._busyTaskCount+=e,this._spinner&&this._busyTaskCount>0&&(this._spinner.active=!0)}finishedTask(){this._busyTaskCount--,this._busyTaskCount<=0&&(this._busyTaskCount=0,this._spinner&&(this._spinner.active=!1),this.dispatchEvent(new CustomEvent("busy-end",{bubbles:!0})))}_addHTML(){let e=this.querySelector("header"),t=e&&e.querySelector("aside");if(!(e&&t&&t.classList.contains("hideable")))return;let n=l.content.cloneNode(!0);e.insertBefore(n,e.firstElementChild),(n=e.firstElementChild).addEventListener("click",e=>this._toggleMenu(e,t));let s=a.content.cloneNode(!0);e.insertBefore(s,t),this._spinner=e.querySelector("spinner-sk");let i=document.createElement("span");i.classList.add("grow"),e.appendChild(i),this._loginEle=document.createElement("div"),e.appendChild(this._loginEle)}_toggleMenu(e,t){t.classList.toggle("shown")}_render(){this._loginEle&&Object(s.b)((e=>s["a"]` <oauth-login client_id=${e.client_id} testing_offline=${e.testing_offline}></oauth-login> `)(this),this._loginEle)}attributeChangedCallback(e,t,n){this._render()}});n(11)},,,,,function(e,t,n){"use strict";n.r(t);n(3)},,,function(e,t){},function(e,t){},function(e,t){},,function(e,t){}]);