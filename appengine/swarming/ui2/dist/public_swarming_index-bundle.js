!function(t){var e={};function s(i){if(e[i])return e[i].exports;var n=e[i]={i:i,l:!1,exports:{}};return t[i].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=t,s.c=e,s.d=function(t,e,i){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},s.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(s.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)s.d(i,n,function(e){return t[e]}.bind(null,n));return i},s.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="/newres/",s(s.s=61)}([function(t,e,s){"use strict";s.d(e,"b",(function(){return o.a})),s.d(e,"a",(function(){return i.b})),s.d(e,"d",(function(){return d})),s.d(e,"c",(function(){return p}));var i=s(3);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const n=new class{handleAttributeExpressions(t,e,s,n){const r=e[0];if("."===r){return new i.f(t,e.slice(1),s).parts}return"@"===r?[new i.d(t,e.slice(1),n.eventContext)]:"?"===r?[new i.c(t,e.slice(1),s)]:new i.a(t,e,s).parts}handleTextExpression(t){return new i.e(t)}};var r=s(12),o=s(11),a=s(8),l=(s(5),s(2));
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
function c(t){let e=h.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},h.set(t.type,e));let s=e.stringsArray.get(t.strings);if(void 0!==s)return s;const i=t.strings.join(l.f);return s=e.keyString.get(i),void 0===s&&(s=new l.a(t,t.getTemplateElement()),e.keyString.set(i,s)),e.stringsArray.set(t.strings,s),s}const h=new Map,u=new WeakMap,d=(t,e,s)=>{let n=u.get(e);void 0===n&&(Object(a.b)(e,e.firstChild),u.set(e,n=new i.e(Object.assign({templateFactory:c},s))),n.appendInto(e)),n.setValue(t),n.commit()};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */s(16);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.0.0");const p=(t,...e)=>new r.b(t,e,"html",n)},function(t,e,s){"use strict";function i(t,e){if(t.hasOwnProperty(e)){let s=t[e];delete t[e],t[e]=s}}s.d(e,"a",(function(){return i}))},function(t,e,s){"use strict";s.d(e,"f",(function(){return i})),s.d(e,"g",(function(){return n})),s.d(e,"b",(function(){return o})),s.d(e,"a",(function(){return a})),s.d(e,"d",(function(){return l})),s.d(e,"c",(function(){return c})),s.d(e,"e",(function(){return h}));
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const i=`{{lit-${String(Math.random()).slice(2)}}}`,n=`\x3c!--${i}--\x3e`,r=new RegExp(`${i}|${n}`),o="$lit$";class a{constructor(t,e){this.parts=[],this.element=e;let s=-1,n=0;const a=[],l=e=>{const u=e.content,d=document.createTreeWalker(u,133,null,!1);let p=0;for(;d.nextNode();){s++;const e=d.currentNode;if(1===e.nodeType){if(e.hasAttributes()){const a=e.attributes;let l=0;for(let t=0;t<a.length;t++)a[t].value.indexOf(i)>=0&&l++;for(;l-- >0;){const i=t.strings[n],a=h.exec(i)[2],l=a.toLowerCase()+o,c=e.getAttribute(l).split(r);this.parts.push({type:"attribute",index:s,name:a,strings:c}),e.removeAttribute(l),n+=c.length-1}}"TEMPLATE"===e.tagName&&l(e)}else if(3===e.nodeType){const t=e.data;if(t.indexOf(i)>=0){const i=e.parentNode,o=t.split(r),l=o.length-1;for(let t=0;t<l;t++)i.insertBefore(""===o[t]?c():document.createTextNode(o[t]),e),this.parts.push({type:"node",index:++s});""===o[l]?(i.insertBefore(c(),e),a.push(e)):e.data=o[l],n+=l}}else if(8===e.nodeType)if(e.data===i){const t=e.parentNode;null!==e.previousSibling&&s!==p||(s++,t.insertBefore(c(),e)),p=s,this.parts.push({type:"node",index:s}),null===e.nextSibling?e.data="":(a.push(e),s--),n++}else{let t=-1;for(;-1!==(t=e.data.indexOf(i,t+1));)this.parts.push({type:"node",index:-1})}}};l(e);for(const t of a)t.parentNode.removeChild(t)}}const l=t=>-1!==t.index,c=()=>document.createComment(""),h=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F \x09\x0a\x0c\x0d"'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/},function(t,e,s){"use strict";s.d(e,"g",(function(){return c})),s.d(e,"a",(function(){return h})),s.d(e,"b",(function(){return u})),s.d(e,"e",(function(){return d})),s.d(e,"c",(function(){return p})),s.d(e,"f",(function(){return f})),s.d(e,"d",(function(){return g}));var i=s(11),n=s(8),r=s(5),o=s(16),a=s(12),l=s(2);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const c=t=>null===t||!("object"==typeof t||"function"==typeof t);class h{constructor(t,e,s){this.dirty=!0,this.element=t,this.name=e,this.strings=s,this.parts=[];for(let t=0;t<s.length-1;t++)this.parts[t]=this._createPart()}_createPart(){return new u(this)}_getValue(){const t=this.strings,e=t.length-1;let s="";for(let i=0;i<e;i++){s+=t[i];const e=this.parts[i];if(void 0!==e){const t=e.value;if(null!=t&&(Array.isArray(t)||"string"!=typeof t&&t[Symbol.iterator]))for(const e of t)s+="string"==typeof e?e:String(e);else s+="string"==typeof t?t:String(t)}}return s+=t[e],s}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class u{constructor(t){this.value=void 0,this.committer=t}setValue(t){t===r.a||c(t)&&t===this.value||(this.value=t,Object(i.b)(t)||(this.committer.dirty=!0))}commit(){for(;Object(i.b)(this.value);){const t=this.value;this.value=r.a,t(this)}this.value!==r.a&&this.committer.commit()}}class d{constructor(t){this.value=void 0,this._pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(Object(l.c)()),this.endNode=t.appendChild(Object(l.c)())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t._insert(this.startNode=Object(l.c)()),t._insert(this.endNode=Object(l.c)())}insertAfterPart(t){t._insert(this.startNode=Object(l.c)()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this._pendingValue=t}commit(){for(;Object(i.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}const t=this._pendingValue;t!==r.a&&(c(t)?t!==this.value&&this._commitText(t):t instanceof a.b?this._commitTemplateResult(t):t instanceof Node?this._commitNode(t):Array.isArray(t)||t[Symbol.iterator]?this._commitIterable(t):t===r.b?(this.value=r.b,this.clear()):this._commitText(t))}_insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}_commitNode(t){this.value!==t&&(this.clear(),this._insert(t),this.value=t)}_commitText(t){const e=this.startNode.nextSibling;t=null==t?"":t,e===this.endNode.previousSibling&&3===e.nodeType?e.data=t:this._commitNode(document.createTextNode("string"==typeof t?t:String(t))),this.value=t}_commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof o.a&&this.value.template===e)this.value.update(t.values);else{const s=new o.a(e,t.processor,this.options),i=s._clone();s.update(t.values),this._commitNode(i),this.value=s}}_commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let s,i=0;for(const n of t)s=e[i],void 0===s&&(s=new d(this.options),e.push(s),0===i?s.appendIntoPart(this):s.insertAfterPart(e[i-1])),s.setValue(n),s.commit(),i++;i<e.length&&(e.length=i,this.clear(s&&s.endNode))}clear(t=this.startNode){Object(n.b)(this.startNode.parentNode,t.nextSibling,this.endNode)}}class p{constructor(t,e,s){if(this.value=void 0,this._pendingValue=void 0,2!==s.length||""!==s[0]||""!==s[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=s}setValue(t){this._pendingValue=t}commit(){for(;Object(i.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}if(this._pendingValue===r.a)return;const t=!!this._pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)),this.value=t,this._pendingValue=r.a}}class f extends h{constructor(t,e,s){super(t,e,s),this.single=2===s.length&&""===s[0]&&""===s[1]}_createPart(){return new _(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class _ extends u{}let m=!1;try{const t={get capture(){return m=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}class g{constructor(t,e,s){this.value=void 0,this._pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=s,this._boundHandleEvent=t=>this.handleEvent(t)}setValue(t){this._pendingValue=t}commit(){for(;Object(i.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}if(this._pendingValue===r.a)return;const t=this._pendingValue,e=this.value,s=null==t||null!=e&&(t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive),n=null!=t&&(null==e||s);s&&this.element.removeEventListener(this.eventName,this._boundHandleEvent,this._options),n&&(this._options=v(t),this.element.addEventListener(this.eventName,this._boundHandleEvent,this._options)),this.value=t,this._pendingValue=r.a}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const v=t=>t&&(m?{capture:t.capture,passive:t.passive,once:t.once}:t.capture)},,function(t,e,s){"use strict";s.d(e,"a",(function(){return i})),s.d(e,"b",(function(){return n}));
/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const i={},n={}},,function(t,e,s){"use strict";function i(t,e=1e4){"object"==typeof t&&(t=t.message||JSON.stringify(t));var s={message:t,duration:e};document.dispatchEvent(new CustomEvent("error-sk",{detail:s,bubbles:!0}))}s.d(e,"a",(function(){return i}))},function(t,e,s){"use strict";s.d(e,"a",(function(){return i})),s.d(e,"c",(function(){return n})),s.d(e,"b",(function(){return r}));
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const i=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,n=(t,e,s=null,i=null)=>{let n=e;for(;n!==s;){const e=n.nextSibling;t.insertBefore(n,i),n=e}},r=(t,e,s=null)=>{let i=e;for(;i!==s;){const e=i.nextSibling;t.removeChild(i),i=e}}},function(t,e,s){"use strict";function i(t){if(t.ok)return t.json();throw{message:`Bad network response: ${t.statusText}`,resp:t,status:t.status}}s.d(e,"a",(function(){return i}))},,function(t,e,s){"use strict";s.d(e,"a",(function(){return n})),s.d(e,"b",(function(){return r}));
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const i=new WeakMap,n=t=>(...e)=>{const s=t(...e);return i.set(s,!0),s},r=t=>"function"==typeof t&&i.has(t)},function(t,e,s){"use strict";s.d(e,"b",(function(){return r})),s.d(e,"a",(function(){return o}));var i=s(8),n=s(2);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
class r{constructor(t,e,s,i){this.strings=t,this.values=e,this.type=s,this.processor=i}getHTML(){const t=this.strings.length-1;let e="";for(let s=0;s<t;s++){const t=this.strings[s],i=n.e.exec(t);e+=i?t.substr(0,i.index)+i[1]+i[2]+n.b+i[3]+n.f:t+n.g}return e+this.strings[t]}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}class o extends r{getHTML(){return`<svg>${super.getHTML()}</svg>`}getTemplateElement(){const t=super.getTemplateElement(),e=t.content,s=e.firstChild;return e.removeChild(s),Object(i.c)(e,s.firstChild),t}}},,function(t,e,s){},,function(t,e,s){"use strict";s.d(e,"a",(function(){return r}));var i=s(8),n=s(2);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
class r{constructor(t,e,s){this._parts=[],this.template=t,this.processor=e,this.options=s}update(t){let e=0;for(const s of this._parts)void 0!==s&&s.setValue(t[e]),e++;for(const t of this._parts)void 0!==t&&t.commit()}_clone(){const t=i.a?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=this.template.parts;let s=0,r=0;const o=t=>{const i=document.createTreeWalker(t,133,null,!1);let a=i.nextNode();for(;s<e.length&&null!==a;){const t=e[s];if(Object(n.d)(t))if(r===t.index){if("node"===t.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(a.previousSibling),this._parts.push(t)}else this._parts.push(...this.processor.handleAttributeExpressions(a,t.name,t.strings,this.options));s++}else r++,"TEMPLATE"===a.nodeName&&o(a.content),a=i.nextNode();else this._parts.push(void 0),s++}};return o(t),i.a&&(document.adoptNode(t),customElements.upgrade(t)),t}}},function(t,e,s){"use strict";s.d(e,"a",(function(){return n}));var i=s(0);
/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const n=Object(i.b)(t=>e=>{if(void 0===t&&e instanceof i.a){if(t!==e.value){const t=e.committer.name;e.committer.element.removeAttribute(t)}}else e.setValue(t)})},,,,function(t,e,s){"use strict";s.d(e,"a",(function(){return o}));var i=s(7),n=s(0),r=s(1);class o extends HTMLElement{constructor(t){super(),this._template=t,this._app=null,this._auth_header="",this._profile=null,this._notAuthorized=!1}connectedCallback(){Object(r.a)(this,"client_id"),Object(r.a)(this,"testing_offline"),this._authHeaderEvent=t=>{this._auth_header=t.detail.auth_header},this.addEventListener("log-in",this._authHeaderEvent)}disconnectedCallback(){this.removeEventListener("log-in",this._authHeaderEvent)}static get observedAttributes(){return["client_id","testing_offline"]}get app(){return this._app}get auth_header(){return this._auth_header}get loggedInAndAuthorized(){return!!this._auth_header&&!this._notAuthorized}get permissions(){return this._app&&this._app.permissions||{}}get profile(){return this._app&&this._app.profile||{}}get server_details(){return this._app&&this._app.server_details||{}}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}fetchError(t,e){403===t.status?(this._message="User unauthorized - try logging in with a different account",this._notAuthorized=!0,this.render()):"AbortError"!==t.name&&(console.error(t),Object(i.a)(`Unexpected error loading ${e}: ${t.message}`,5e3)),this._app.finishedTask()}render(){Object(n.d)(this._template(this),this,{eventContext:this}),this._app||(this._app=this.firstElementChild,Object(n.d)(this._template(this),this,{eventContext:this}))}attributeChangedCallback(t,e,s){this.render()}}},,,,function(t,e,s){},function(t,e,s){},function(t,e,s){},function(t,e,s){},function(t,e,s){"use strict";var i=s(7),n=s(0),r=s(17),o=s(9),a=s(1);window.customElements.define("toast-sk",class extends HTMLElement{constructor(){super(),this._timer=null}connectedCallback(){this.hasAttribute("duration")||(this.duration=5e3),Object(a.a)(this,"duration")}get duration(){return+this.getAttribute("duration")}set duration(t){this.setAttribute("duration",t)}show(){this.setAttribute("shown",""),this.duration>0&&!this._timer&&(this._timer=window.setTimeout(()=>{this._timer=null,this.hide()},this.duration))}hide(){this.removeAttribute("shown"),this._timer&&(window.clearTimeout(this._timer),this._timer=null)}});s(25);window.customElements.define("error-toast-sk",class extends HTMLElement{connectedCallback(){this.innerHTML="<toast-sk></toast-sk>",this._toast=this.firstElementChild,document.addEventListener("error-sk",this)}disconnectedCallback(){document.removeEventListener("error-sk",this)}handleEvent(t){t.detail.duration&&(this._toast.duration=t.detail.duration),this._toast.textContent=t.detail.message,this._toast.show()}});s(14);const l=document.createElement("template");l.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M20 8h-2.81c-.45-.78-1.07-1.45-1.82-1.96L17 4.41 15.59 3l-2.17 2.17C12.96 5.06 12.49 5 12 5c-.49 0-.96.06-1.41.17L8.41 3 7 4.41l1.62 1.63C7.88 6.55 7.26 7.22 6.81 8H4v2h2.09c-.05.33-.09.66-.09 1v1H4v2h2v1c0 .34.04.67.09 1H4v2h2.81c1.04 1.79 2.97 3 5.19 3s4.15-1.21 5.19-3H20v-2h-2.09c.05-.33.09-.66.09-1v-1h2v-2h-2v-1c0-.34-.04-.67-.09-1H20V8zm-6 8h-4v-2h4v2zm0-4h-4v-2h4v2z"/></svg>',window.customElements.define("bug-report-icon-sk",class extends HTMLElement{connectedCallback(){let t=l.content.cloneNode(!0);this.appendChild(t)}});const c=document.createElement("template");c.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>',window.customElements.define("menu-icon-sk",class extends HTMLElement{connectedCallback(){let t=c.content.cloneNode(!0);this.appendChild(t)}}),window.customElements.define("spinner-sk",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"active")}get active(){return this.hasAttribute("active")}set active(t){t?this.setAttribute("active",""):this.removeAttribute("active")}});s(26),s(27);const h=new Promise((t,e)=>{const s=()=>{void 0!==window.gapi?t():setTimeout(s,10)};setTimeout(s,10)});window.customElements.define("oauth-login",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._auth_header="",this.testing_offline?this._profile={email:"missing@chromium.org",imageURL:"http://storage.googleapis.com/gd-wagtail-prod-assets/original_images/logo_google_fonts_color_2x_web_64dp.png"}:(this._profile=null,h.then(()=>{gapi.load("auth2",()=>{gapi.auth2.init({client_id:this.client_id}).then(()=>{this._maybeFireLoginEvent(),this.render()},t=>{console.error(t),Object(i.a)(`Error initializing oauth: ${JSON.stringify(t)}`,1e4)})})})),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get auth_header(){return this._auth_header}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get profile(){return this._profile}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}_maybeFireLoginEvent(){const t=gapi.auth2.getAuthInstance().currentUser.get();if(t.isSignedIn()){const e=t.getBasicProfile();this._profile={email:e.getEmail(),imageURL:e.getImageUrl()};const s=t.getAuthResponse(!0),i=`${s.token_type} ${s.access_token}`;return this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:i,profile:this._profile},bubbles:!0})),this._auth_header=i,!0}return this._profile=null,this._auth_header="",!1}_logIn(){if(this.testing_offline)this._auth_header="Bearer 12345678910-boomshakalaka",this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:this._auth_header,profile:this._profile},bubbles:!0})),this.render();else{const t=gapi.auth2.getAuthInstance();t&&t.signIn({scope:"email",prompt:"select_account"}).then(()=>{this._maybeFireLoginEvent()||console.warn("login was not successful; maybe user canceled"),this.render()})}}_logOut(){if(this.testing_offline)this._auth_header="",this.render(),window.location.reload();else{const t=gapi.auth2.getAuthInstance();t&&t.signOut().then(()=>{this._auth_header="",this._profile=null,window.location.reload()})}}render(){var t;Object(n.d)((t=this).auth_header?n.c`
<div>
  <img class=center id=avatar src="${t._profile.imageURL}" width=30 height=30>
  <span class=center>${t._profile.email}</span>
  <span class=center>|</span>
  <a class=center @click=${t._logOut} href="#">Sign out</a>
</div>`:n.c`
<div>
  <a @click=${t._logIn} href="#">Sign in</a>
</div>`,this,{eventContext:this})}attributeChangedCallback(t,e,s){this.render()}});const u=document.createElement("template");u.innerHTML="\n<button class=toggle-button>\n  <menu-icon-sk>\n  </menu-icon-sk>\n</button>\n";const d=document.createElement("template");d.innerHTML="\n<div class=spinner-spacer>\n  <spinner-sk></spinner-sk>\n</div>\n";const p=document.createElement("template");p.innerHTML='\n<a target=_blank rel=noopener\n   href="https://bugs.chromium.org/p/chromium/issues/entry?components=Infra%3EPlatform%3ESwarming%3EWebUI&owner=kjlubick@chromium.org&status=Assigned">\n  <bug-report-icon-sk class=fab></bug-report-icon-sk>\n</a>',window.customElements.define("swarming-app",class extends HTMLElement{constructor(){super(),this._busyTaskCount=0,this._spinner=null,this._dynamicEle=null,this._auth_header="",this._profile={},this._server_details={server_version:"You must log in to see more details",bot_version:""},this._permissions={}}connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._addHTML(),this.addEventListener("log-in",t=>{this._auth_header=t.detail.auth_header,this._profile=t.detail.profile,this._fetch()}),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get busy(){return!!this._busyTaskCount}get permissions(){return this._permissions}get profile(){return this._profile}get server_details(){return this._server_details}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}addBusyTasks(t){this._busyTaskCount+=t,this._spinner&&this._busyTaskCount>0&&(this._spinner.active=!0)}finishedTask(){this._busyTaskCount--,this._busyTaskCount<=0&&(this._busyTaskCount=0,this._spinner&&(this._spinner.active=!1),this.dispatchEvent(new CustomEvent("busy-end",{bubbles:!0})))}_addHTML(){const t=this.querySelector("header"),e=t&&t.querySelector("aside"),s=this.querySelector("footer");if(!(t&&e&&e.classList.contains("hideable")))return;let i=u.content.cloneNode(!0);t.insertBefore(i,t.firstElementChild),i=t.firstElementChild,i.addEventListener("click",t=>this._toggleMenu(t,e));const n=d.content.cloneNode(!0);t.insertBefore(n,e),this._spinner=t.querySelector("spinner-sk");const r=document.createElement("span");r.classList.add("grow"),t.appendChild(r),this._dynamicEle=document.createElement("div"),this._dynamicEle.classList.add("right"),t.appendChild(this._dynamicEle);const o=document.createElement("error-toast-sk");s.append(o);const a=p.content.cloneNode(!0);s.append(a)}_toggleMenu(t,e){e.classList.toggle("shown")}_fetch(){if(!this._auth_header)return;this._server_details={server_version:"<loading>",bot_version:"<loading>"};const t={headers:{authorization:this._auth_header}};this.addBusyTasks(1),fetch("/_ah/api/swarming/v1/server/details",t).then(o.a).then(t=>{this._server_details=t,this.render(),this.dispatchEvent(new CustomEvent("server-details-loaded",{bubbles:!0})),this.finishedTask()}).catch(t=>{403===t.status?(this._server_details={server_version:"User unauthorized - try logging in with a different account",bot_version:""},this.render()):(console.error(t),Object(i.a)(`Unexpected error loading details: ${t.message}`,5e3)),this.finishedTask()}),this._fetchPermissions(t)}_fetchPermissions(t,e){this.addBusyTasks(1);let s="/_ah/api/swarming/v1/server/permissions";if(e){const t=new URLSearchParams;for(const[s,i]of Object.entries(e))t.append(s,i);s+=`?${t.toString()}`}fetch(s,t).then(o.a).then(t=>{this._permissions=t,this.render(),this.dispatchEvent(new CustomEvent("permissions-loaded",{bubbles:!0})),this.finishedTask()}).catch(t=>{403!==t.status&&(console.error(t),Object(i.a)(`Unexpected error loading permissions: ${t.message}`,5e3)),this.finishedTask()})}render(){var t;this._dynamicEle&&Object(n.d)((t=this,n.c`
<div class=server-version>
  Server:
  <a href=${Object(r.a)(function(t){if(t&&t.server_version){var e=t.server_version.split("-");if(2===e.length)return`https://chromium.googlesource.com/infra/luci/luci-py/+/${e[1]}`}}(t._server_details))}>
    ${t._server_details.server_version}
  </a>
</div>
<oauth-login client_id=${t.client_id}
             ?testing_offline=${t.testing_offline}>
</oauth-login>`),this._dynamicEle)}attributeChangedCallback(t,e,s){this.render()}});s(28)},,,,,,,,,,,,,,,,,,,,,,,function(t,e,s){},,,,,,,,,function(t,e,s){"use strict";s.r(e);var i=s(0),n=(s(1),s(9)),r=(s(7),s(21));s(29);const o=t=>{return i.c`
<swarming-app id=swapp
              client_id="${t.client_id}"
              ?testing_offline="${t.testing_offline}">
  <header>
    <div class=title>Swarming</div>
      <aside class=hideable>
        <a href=/>Home</a>
        <a href=/botlist>Bot List</a>
        <a href=/tasklist>Task List</a>
        <a href=/bot>Bot Page</a>
        <a href=/task>Task Page</a>
      </aside>
  </header>
  <main>

    <h2>Service Status</h2>
    <div>Server Version:
      <span class=server_version> ${t.server_details.server_version}</span>
    </div>
    <div>Bot Version: ${t.server_details.bot_version} </div>
    <ul>
      <li>
        <!-- TODO(kjlubick) convert these linked pages to new UI-->
        <a href=/stats>Usage statistics</a>
      </li>
      <li>
        <a href=${(t=>"https://console.cloud.google.com/appengine/instances?"+`project=${t._project_id}&versionId=${t.server_details.server_version}`)(t)}>View version's instances on Cloud Console</a>
      </li>
      <li>
        <a href=${e=t._project_id,`https://console.cloud.google.com/errors?project=${e}`}>View server errors on Cloud Console</a>
      </li>
      <li>
        <a href=${(t=>`https://console.cloud.google.com/logs/viewer?filters=status:500..599&project=${t}`)(t._project_id)}>View logs for HTTP 5xx on Cloud Console</a>
      </li>
      <li>
        <a href="/restricted/ereporter2/report">View ereporter2 report</a>
      </li>
    </ul>

    <h2>Configuration</h2>
    <ul>
      <!-- TODO(kjlubick) convert these linked pages to new UI-->
      <li>
        <a href="/restricted/config">View server config</a>
      </li>
      <li>
        <a href="/restricted/upload/bootstrap">View/upload bootstrap.py</a>
      </li>
      <li>
        <a href="/restricted/upload/bot_config">View/upload bot_config.py</a>
      </li>
      <li>
        <a href="/auth/groups">View/edit user groups</a>
      </li>
    </ul>
    ${t.permissions.get_bootstrap_token?(t=>i.c`
<div>
  <h2>Bootstrapping a bot</h2>
  To bootstrap a bot, run one of these (all links are valid for 1 hour):
  <ol>
    <li>
      <strong> TL;DR; </strong>
<pre class=command>python -c "import urllib; exec urllib.urlopen('${t._host_url}/bootstrap?tok=${t._bootstrap_token}').read()"</pre>
    </li>
    <li>
      Escaped version to pass as a ssh argument:
<pre class=command>'python -c "import urllib; exec urllib.urlopen('"'${t._host_url}/bootstrap?tok=${t._bootstrap_token}'"').read()"'</pre>
    </li>
    <li>
      Manually:
<pre class=command>mkdir bot; cd bot
rm -f swarming_bot.zip; curl -sSLOJ ${t._host_url}/bot_code?tok=${t._bootstrap_token}
python swarming_bot.zip</pre>
    </li>
  </ol>
</div>
`)(t):""}
  </main>
  <footer></footer>
</swarming-app>`;var e};window.customElements.define("swarming-index",class extends r.a{constructor(){super(o),this._bootstrap_token="...";const t=location.hostname.indexOf(".appspot.com");this._project_id=location.hostname.substring(0,t)||"not_found",this._host_url=location.origin}connectedCallback(){super.connectedCallback(),this.addEventListener("permissions-loaded",t=>{this.permissions.get_bootstrap_token&&this._fetchToken(),this.render()}),this.addEventListener("server-details-loaded",t=>{this.render()}),this.render()}_fetchToken(){const t={headers:{authorization:this.auth_header},method:"POST"};this.app.addBusyTasks(1),fetch("/_ah/api/swarming/v1/server/token",t).then(n.a).then(t=>{this._bootstrap_token=t.bootstrap_token,this.render(),this.app.finishedTask()}).catch(t=>this.fetchError(t,"token"))}});s(52)}]);