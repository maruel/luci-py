!function(t){var e={};function s(n){if(e[n])return e[n].exports;var i=e[n]={i:n,l:!1,exports:{}};return t[n].call(i.exports,i,i.exports,s),i.l=!0,i.exports}s.m=t,s.c=e,s.d=function(t,e,n){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},s.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)s.d(n,i,function(e){return t[e]}.bind(null,i));return n},s.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="/newres/",s(s.s=59)}([function(t,e,s){"use strict";s.d(e,"b",(function(){return o.a})),s.d(e,"a",(function(){return n.b})),s.d(e,"d",(function(){return u})),s.d(e,"c",(function(){return _}));var n=s(3);
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
 */const i=new class{handleAttributeExpressions(t,e,s,i){const r=e[0];if("."===r){return new n.f(t,e.slice(1),s).parts}return"@"===r?[new n.d(t,e.slice(1),i.eventContext)]:"?"===r?[new n.c(t,e.slice(1),s)]:new n.a(t,e,s).parts}handleTextExpression(t){return new n.e(t)}};var r=s(12),o=s(11),a=s(8),d=(s(5),s(2));
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
function l(t){let e=c.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},c.set(t.type,e));let s=e.stringsArray.get(t.strings);if(void 0!==s)return s;const n=t.strings.join(d.f);return s=e.keyString.get(n),void 0===s&&(s=new d.a(t,t.getTemplateElement()),e.keyString.set(n,s)),e.stringsArray.set(t.strings,s),s}const c=new Map,h=new WeakMap,u=(t,e,s)=>{let i=h.get(e);void 0===i&&(Object(a.b)(e,e.firstChild),h.set(e,i=new n.e(Object.assign({templateFactory:l},s))),i.appendInto(e)),i.setValue(t),i.commit()};
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
 */(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.0.0");const _=(t,...e)=>new r.b(t,e,"html",i)},function(t,e,s){"use strict";function n(t,e){if(t.hasOwnProperty(e)){let s=t[e];delete t[e],t[e]=s}}s.d(e,"a",(function(){return n}))},function(t,e,s){"use strict";s.d(e,"f",(function(){return n})),s.d(e,"g",(function(){return i})),s.d(e,"b",(function(){return o})),s.d(e,"a",(function(){return a})),s.d(e,"d",(function(){return d})),s.d(e,"c",(function(){return l})),s.d(e,"e",(function(){return c}));
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
const n=`{{lit-${String(Math.random()).slice(2)}}}`,i=`\x3c!--${n}--\x3e`,r=new RegExp(`${n}|${i}`),o="$lit$";class a{constructor(t,e){this.parts=[],this.element=e;let s=-1,i=0;const a=[],d=e=>{const h=e.content,u=document.createTreeWalker(h,133,null,!1);let _=0;for(;u.nextNode();){s++;const e=u.currentNode;if(1===e.nodeType){if(e.hasAttributes()){const a=e.attributes;let d=0;for(let t=0;t<a.length;t++)a[t].value.indexOf(n)>=0&&d++;for(;d-- >0;){const n=t.strings[i],a=c.exec(n)[2],d=a.toLowerCase()+o,l=e.getAttribute(d).split(r);this.parts.push({type:"attribute",index:s,name:a,strings:l}),e.removeAttribute(d),i+=l.length-1}}"TEMPLATE"===e.tagName&&d(e)}else if(3===e.nodeType){const t=e.data;if(t.indexOf(n)>=0){const n=e.parentNode,o=t.split(r),d=o.length-1;for(let t=0;t<d;t++)n.insertBefore(""===o[t]?l():document.createTextNode(o[t]),e),this.parts.push({type:"node",index:++s});""===o[d]?(n.insertBefore(l(),e),a.push(e)):e.data=o[d],i+=d}}else if(8===e.nodeType)if(e.data===n){const t=e.parentNode;null!==e.previousSibling&&s!==_||(s++,t.insertBefore(l(),e)),_=s,this.parts.push({type:"node",index:s}),null===e.nextSibling?e.data="":(a.push(e),s--),i++}else{let t=-1;for(;-1!==(t=e.data.indexOf(n,t+1));)this.parts.push({type:"node",index:-1})}}};d(e);for(const t of a)t.parentNode.removeChild(t)}}const d=t=>-1!==t.index,l=()=>document.createComment(""),c=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F \x09\x0a\x0c\x0d"'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/},function(t,e,s){"use strict";s.d(e,"g",(function(){return l})),s.d(e,"a",(function(){return c})),s.d(e,"b",(function(){return h})),s.d(e,"e",(function(){return u})),s.d(e,"c",(function(){return _})),s.d(e,"f",(function(){return p})),s.d(e,"d",(function(){return b}));var n=s(11),i=s(8),r=s(5),o=s(16),a=s(12),d=s(2);
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
const l=t=>null===t||!("object"==typeof t||"function"==typeof t);class c{constructor(t,e,s){this.dirty=!0,this.element=t,this.name=e,this.strings=s,this.parts=[];for(let t=0;t<s.length-1;t++)this.parts[t]=this._createPart()}_createPart(){return new h(this)}_getValue(){const t=this.strings,e=t.length-1;let s="";for(let n=0;n<e;n++){s+=t[n];const e=this.parts[n];if(void 0!==e){const t=e.value;if(null!=t&&(Array.isArray(t)||"string"!=typeof t&&t[Symbol.iterator]))for(const e of t)s+="string"==typeof e?e:String(e);else s+="string"==typeof t?t:String(t)}}return s+=t[e],s}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class h{constructor(t){this.value=void 0,this.committer=t}setValue(t){t===r.a||l(t)&&t===this.value||(this.value=t,Object(n.b)(t)||(this.committer.dirty=!0))}commit(){for(;Object(n.b)(this.value);){const t=this.value;this.value=r.a,t(this)}this.value!==r.a&&this.committer.commit()}}class u{constructor(t){this.value=void 0,this._pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(Object(d.c)()),this.endNode=t.appendChild(Object(d.c)())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t._insert(this.startNode=Object(d.c)()),t._insert(this.endNode=Object(d.c)())}insertAfterPart(t){t._insert(this.startNode=Object(d.c)()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this._pendingValue=t}commit(){for(;Object(n.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}const t=this._pendingValue;t!==r.a&&(l(t)?t!==this.value&&this._commitText(t):t instanceof a.b?this._commitTemplateResult(t):t instanceof Node?this._commitNode(t):Array.isArray(t)||t[Symbol.iterator]?this._commitIterable(t):t===r.b?(this.value=r.b,this.clear()):this._commitText(t))}_insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}_commitNode(t){this.value!==t&&(this.clear(),this._insert(t),this.value=t)}_commitText(t){const e=this.startNode.nextSibling;t=null==t?"":t,e===this.endNode.previousSibling&&3===e.nodeType?e.data=t:this._commitNode(document.createTextNode("string"==typeof t?t:String(t))),this.value=t}_commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof o.a&&this.value.template===e)this.value.update(t.values);else{const s=new o.a(e,t.processor,this.options),n=s._clone();s.update(t.values),this._commitNode(n),this.value=s}}_commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let s,n=0;for(const i of t)s=e[n],void 0===s&&(s=new u(this.options),e.push(s),0===n?s.appendIntoPart(this):s.insertAfterPart(e[n-1])),s.setValue(i),s.commit(),n++;n<e.length&&(e.length=n,this.clear(s&&s.endNode))}clear(t=this.startNode){Object(i.b)(this.startNode.parentNode,t.nextSibling,this.endNode)}}class _{constructor(t,e,s){if(this.value=void 0,this._pendingValue=void 0,2!==s.length||""!==s[0]||""!==s[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=s}setValue(t){this._pendingValue=t}commit(){for(;Object(n.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}if(this._pendingValue===r.a)return;const t=!!this._pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)),this.value=t,this._pendingValue=r.a}}class p extends c{constructor(t,e,s){super(t,e,s),this.single=2===s.length&&""===s[0]&&""===s[1]}_createPart(){return new f(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class f extends h{}let m=!1;try{const t={get capture(){return m=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}class b{constructor(t,e,s){this.value=void 0,this._pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=s,this._boundHandleEvent=t=>this.handleEvent(t)}setValue(t){this._pendingValue=t}commit(){for(;Object(n.b)(this._pendingValue);){const t=this._pendingValue;this._pendingValue=r.a,t(this)}if(this._pendingValue===r.a)return;const t=this._pendingValue,e=this.value,s=null==t||null!=e&&(t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive),i=null!=t&&(null==e||s);s&&this.element.removeEventListener(this.eventName,this._boundHandleEvent,this._options),i&&(this._options=g(t),this.element.addEventListener(this.eventName,this._boundHandleEvent,this._options)),this.value=t,this._pendingValue=r.a}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const g=t=>t&&(m?{capture:t.capture,passive:t.passive,once:t.once}:t.capture)},function(t,e,s){"use strict";s.d(e,"b",(function(){return o})),s.d(e,"a",(function(){return a})),s.d(e,"c",(function(){return d})),s.d(e,"d",(function(){return l})),s.d(e,"e",(function(){return c})),s.d(e,"f",(function(){return h})),s.d(e,"g",(function(){return u})),s.d(e,"h",(function(){return _})),s.d(e,"i",(function(){return p})),s.d(e,"j",(function(){return f})),s.d(e,"k",(function(){return m})),s.d(e,"l",(function(){return b}));var n=s(13),i=s(10),r=s(1);function o(t){if(t)return"/bot?id="+t}function a(t=[],e=[]){const s=[];for(const e of t)if(e.key&&e.value)if(Array.isArray(e.value))for(const t of e.value)s.push(e.key+":"+t);else s.push(e.key+":"+e.value);else s.push(e);const n={f:s,c:e};return"/botlist?"+i.b(n)}function d(t){return t||(t=[]),function(e,s){let n=t.indexOf(e);-1===n&&(n=t.length+1);let i=t.indexOf(s);return-1===i&&(i=t.length+1),n===i?e.localeCompare(s):n-i}}function l(t){if(0===t||"0"===t)return"0s";if(!t)return"--";const e=parseFloat(t);return e?e>60?n.e(e):e.toFixed(2)+"s":t+" seconds"}function c(t,e,s=!0){Object(r.a)(t,e),void 0===t[e]&&t.hasAttribute(e)&&(t[e]=t.getAttribute(e),s&&t.removeAttribute(e))}function h(){return window.innerWidth<600||window.innerHeight<600}function u(t){let e=t.slice(0,-1);if(!/[1-9][0-9]*/.test(e))return null;switch(e=parseInt(e),t.slice(-1)){case"h":e*=60;case"m":e*=60;case"s":break;default:return null}return e}function _(t,e){if(t["human_"+e]="--",t[e]){t[e].endsWith&&!t[e].endsWith("Z")&&(t[e]+="Z"),t[e]=new Date(t[e]);const s=t[e].toString(),n=s.substring(s.indexOf("("));t["human_"+e]=t[e].toLocaleString()+" "+n}}function p(t=[],e=[]){const s=[];for(const e of t)if(e.key&&e.value)if(Array.isArray(e.value))for(const t of e.value)s.push(e.key+":"+t);else s.push(e.key+":"+e.value);else s.push(e);for(let t=2;t<arguments.length;t++)s.push(arguments[t]);const n={f:s,c:e};return"/tasklist?"+i.b(n)}function f(t,e){if(t)return e||(t=t.substring(0,t.length-1)+"0"),`/task?id=${t}`}function m(t){return t?n.c(t.getTime())||"0s":"eons"}function b(t,e){return t?(e||(e=new Date),n.e((e.getTime()-t.getTime())/1e3)||"0s"):"eons"}},function(t,e,s){"use strict";s.d(e,"a",(function(){return n})),s.d(e,"b",(function(){return i}));
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
const n={},i={}},function(t,e,s){"use strict";s.d(e,"c",(function(){return n})),s.d(e,"a",(function(){return i})),s.d(e,"b",(function(){return r}));const n=new Promise((function(t,e){"loading"!==document.readyState?t():document.addEventListener("DOMContentLoaded",t)})),i=(t,e=document)=>Array.prototype.slice.call(e.querySelectorAll(t)),r=(t,e=document)=>e.querySelector(t)},function(t,e,s){"use strict";function n(t,e=1e4){"object"==typeof t&&(t=t.message||JSON.stringify(t));var s={message:t,duration:e};document.dispatchEvent(new CustomEvent("error-sk",{detail:s,bubbles:!0}))}s.d(e,"a",(function(){return n}))},function(t,e,s){"use strict";s.d(e,"a",(function(){return n})),s.d(e,"c",(function(){return i})),s.d(e,"b",(function(){return r}));
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
const n=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,i=(t,e,s=null,n=null)=>{let i=e;for(;i!==s;){const e=i.nextSibling;t.insertBefore(i,n),i=e}},r=(t,e,s=null)=>{let n=e;for(;n!==s;){const e=n.nextSibling;t.removeChild(n),n=e}}},function(t,e,s){"use strict";function n(t){if(t.ok)return t.json();throw{message:`Bad network response: ${t.statusText}`,resp:t,status:t.status}}s.d(e,"a",(function(){return n}))},function(t,e,s){"use strict";function n(t){if(!t)return"";var e=[];return Object.keys(t).sort().forEach((function(s){t[s].forEach((function(t){e.push(encodeURIComponent(s)+"="+encodeURIComponent(t))}))})),e.join("&")}function i(t){var e=[];return Object.keys(t).sort().forEach((function(s){Array.isArray(t[s])?t[s].forEach((function(t){e.push(encodeURIComponent(s)+"="+encodeURIComponent(t))})):"object"==typeof t[s]?e.push(encodeURIComponent(s)+"="+encodeURIComponent(i(t[s]))):e.push(encodeURIComponent(s)+"="+encodeURIComponent(t[s]))})),e.join("&")}function r(t,e){e=e||{};for(var s={},n=t.split("&"),i=0;i<n.length;i++){var o=n[i].split("=",2);if(2==o.length){var a=decodeURIComponent(o[0]),d=decodeURIComponent(o[1]);if(e.hasOwnProperty(a))switch(typeof e[a]){case"boolean":s[a]="true"==d;break;case"number":s[a]=Number(d);break;case"object":if(Array.isArray(e[a])){var l=s[a]||[];l.push(d),s[a]=l}else s[a]=r(d,e[a]);break;case"string":s[a]=d;break;default:s[a]=d}else s[a]=d}}return s}s.d(e,"b",(function(){return n})),s.d(e,"a",(function(){return i})),s.d(e,"c",(function(){return r}))},function(t,e,s){"use strict";s.d(e,"a",(function(){return i})),s.d(e,"b",(function(){return r}));
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
const n=new WeakMap,i=t=>(...e)=>{const s=t(...e);return n.set(s,!0),s},r=t=>"function"==typeof t&&n.has(t)},function(t,e,s){"use strict";s.d(e,"b",(function(){return r})),s.d(e,"a",(function(){return o}));var n=s(8),i=s(2);
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
class r{constructor(t,e,s,n){this.strings=t,this.values=e,this.type=s,this.processor=n}getHTML(){const t=this.strings.length-1;let e="";for(let s=0;s<t;s++){const t=this.strings[s],n=i.e.exec(t);e+=n?t.substr(0,n.index)+n[1]+n[2]+i.b+n[3]+i.f:t+i.g}return e+this.strings[t]}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}class o extends r{getHTML(){return`<svg>${super.getHTML()}</svg>`}getTemplateElement(){const t=super.getTemplateElement(),e=t.content,s=e.firstChild;return e.removeChild(s),Object(n.c)(e,s.firstChild),t}}},function(t,e,s){"use strict";s.d(e,"a",(function(){return i})),s.d(e,"e",(function(){return d})),s.d(e,"c",(function(){return l})),s.d(e,"b",(function(){return c})),s.d(e,"d",(function(){return h}));const n=[{units:"w",delta:604800},{units:"d",delta:86400},{units:"h",delta:3600},{units:"m",delta:60},{units:"s",delta:1}],i=1048576,r=1024*i,o=1024*r,a=[{units:" PB",delta:1024*o},{units:" TB",delta:o},{units:" GB",delta:r},{units:" MB",delta:i},{units:" KB",delta:1024},{units:" B",delta:1}];function d(t){if(t<0&&(t=-t),0===t)return"  0s";let e="";for(let s=0;s<n.length;s++)if(n[s].delta<=t){let i=Math.floor(t/n[s].delta)+n[s].units;for(;i.length<4;)i=" "+i;e+=i,t%=n[s].delta}return e}function l(t){let e=(("number"==typeof t?t:Date.parse(t))-Date.now())/1e3;return e<0&&(e*=-1),u(e,n)}function c(t,e=1){return Number.isInteger(e)&&(t*=e),u(t,a)}function h(t){let e=t.toString(),s=e.substring(e.indexOf("("));return t.toLocaleString()+" "+s}function u(t,e){for(let s=0;s<e.length-1;s++){if(Math.round(t/e[s+1].delta)*e[s+1].delta/e[s].delta>=1)return Math.round(t/e[s].delta)+e[s].units}let s=e.length-1;return Math.round(t/e[s].delta)+e[s].units}},function(t,e,s){},function(t,e,s){"use strict";s.d(e,"a",(function(){return o})),s.d(e,"b",(function(){return a})),s.d(e,"c",(function(){return d})),s.d(e,"d",(function(){return l})),s.d(e,"e",(function(){return c})),s.d(e,"f",(function(){return h})),s.d(e,"h",(function(){return u})),s.d(e,"g",(function(){return _})),s.d(e,"i",(function(){return p})),s.d(e,"j",(function(){return f})),s.d(e,"k",(function(){return m})),s.d(e,"l",(function(){return b})),s.d(e,"m",(function(){return g})),s.d(e,"n",(function(){return v})),s.d(e,"p",(function(){return k})),s.d(e,"o",(function(){return w})),s.d(e,"q",(function(){return E})),s.d(e,"r",(function(){return y}));var n=s(13),i=s(4),r=s(20);function o(t){return t&&t.properties&&t.properties.idempotent}function a(t,e){if(!t||!e)return;const s=t.split(":");return 2===s.length?`${e}/p/${s[0]}/+/${s[1]}`:void 0}function d(t){let e=0,s=0;return t.performance_stats&&(s=t.performance_stats.isolated_upload&&t.performance_stats.isolated_upload.duration||0,e=t.performance_stats.bot_overhead-s),[t.pending,e,t.duration,s].map((function(t){return t?Math.round(10*t)/10:0}))}function l(t,e){const s=t.filter((function(t){return t.key===e}));if(!s.length)return null;const n=s[0].value;return n.length?n[0]:null}function c(t){if(!t||!t._request||!t._request.tagMap)return!1;const e=t._request.tagMap;return e.allow_milo||e.luci_project}function h(t,e){if(!t||!t.state)return"";if(void 0!==e&&t.current_task_slice!==e)return"THIS SLICE DID NOT RUN. Select another slice above.";const s=t.state;return"COMPLETED"===s?t.failure?"COMPLETED (FAILURE)":E(t)?"COMPLETED (DEDUPED)":"COMPLETED (SUCCESS)":s}function u(t){return t.isolatedserver+"/browse?namespace="+t.namespace+"&hash="+t.isolated}function _(t){return t&&t.endsWith(0)}function p(t){if(!t)return{};t.tagMap={},t.tags=t.tags||[];for(const e of t.tags){const s=e.split(":",1)[0],n=e.substring(s.length+1);t.tagMap[s]=n}return $.forEach(e=>{Object(i.h)(t,e)}),t}function f(t){if(!t)return{};$.forEach(e=>{Object(i.h)(t,e)}),t.try_number&&(t.try_number=+t.try_number);const e=new Date;!t.duration&&"RUNNING"===t.state&&t.started_ts?t.duration=(e-t.started_ts)/1e3:!t.duration&&"BOT_DIED"===t.state&&t.started_ts&&t.abandoned_ts&&(t.duration=(t.abandoned_ts-t.started_ts)/1e3),t.human_duration=Object(i.d)(t.duration),"RUNNING"===t.state?t.human_duration+="*":"BOT_DIED"===t.state&&(t.human_duration+=" -- died");const s=t.started_ts||t.abandoned_ts||new Date;return t.created_ts?s<=t.created_ts?(t.pending=0,t.human_pending="0s"):(t.pending=(s-t.created_ts)/1e3,t.human_pending=Object(i.l)(t.created_ts,s)):(t.pending=0,t.human_pending=""),t.current_task_slice=parseInt(t.current_task_slice)||0,t}function m(t){if(!t||!t._request||!t._request.tagMap)return;const e=t._request.tagMap,s=e.milo_host;let n=e.log_location;if(n&&s){if(n=n.replace("logdog://",""),-1!==n.indexOf("${SWARMING_TASK_ID}")){if(!t._result||!t._result.run_id)return;n=n.replace("${SWARMING_TASK_ID}",t._result.run_id)}return s.replace("%s",n)}const i=t.server_details.display_server_url_template;return i&&t._taskId?i.replace("%s",t._taskId):void 0}function b(t,e){if(!e.created_ts)return"";const s=1e3*t.expiration_secs;return n.d(new Date(e.created_ts.getTime()+s))}function g(t){if(!t||!t.state)return"";const e=t.state;return r.b.has(e)?"exception":"BOT_DIED"===e?"bot_died":r.d.has(e)?"pending_task":"COMPLETED"===e&&t.failure?"failed_task":""}function v(t){return t&&t.costs_usd&&t.costs_usd.length?t.costs_usd[0].toFixed(4):0}function k(t){if(!t.created_ts)return"";const e=1e3*t.expiration_secs;return n.d(new Date(t.created_ts.getTime()+e))}function w(t,e){return t&&e&&-1!==t._currentSliceIdx&&t._currentSliceIdx!==e.current_task_slice?"inactive":""}function E(t){return 0===t.try_number}function y(t){return t&&"PENDING"!==t.state&&"NO_RESOURCE"!==t.state&&"CANCELED"!==t.state&&"EXPIRED"!==t.state}const $=["abandoned_ts","completed_ts","created_ts","modified_ts","started_ts"]},function(t,e,s){"use strict";s.d(e,"a",(function(){return r}));var n=s(8),i=s(2);
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
class r{constructor(t,e,s){this._parts=[],this.template=t,this.processor=e,this.options=s}update(t){let e=0;for(const s of this._parts)void 0!==s&&s.setValue(t[e]),e++;for(const t of this._parts)void 0!==t&&t.commit()}_clone(){const t=n.a?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=this.template.parts;let s=0,r=0;const o=t=>{const n=document.createTreeWalker(t,133,null,!1);let a=n.nextNode();for(;s<e.length&&null!==a;){const t=e[s];if(Object(i.d)(t))if(r===t.index){if("node"===t.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(a.previousSibling),this._parts.push(t)}else this._parts.push(...this.processor.handleAttributeExpressions(a,t.name,t.strings,this.options));s++}else r++,"TEMPLATE"===a.nodeName&&o(a.content),a=n.nextNode();else this._parts.push(void 0),s++}};return o(t),n.a&&(document.adoptNode(t),customElements.upgrade(t)),t}}},function(t,e,s){"use strict";s.d(e,"a",(function(){return i}));var n=s(0);
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
 */const i=Object(n.b)(t=>e=>{if(void 0===t&&e instanceof n.a){if(t!==e.value){const t=e.committer.name;e.committer.element.removeAttribute(t)}}else e.setValue(t)})},function(t,e,s){"use strict";function n(t,e){if(!i[e]||"none"===t||!t)return t;let s=i[e][t];if("gpu"===e){const n=t.split("-")[0];s=i[e][n]}else if("os"===e){const n=t.split(".")[0];s=i[e][n]}return s?`${s} (${t})`:t}s.d(e,"a",(function(){return n})),s.d(e,"b",(function(){return o})),s.d(e,"c",(function(){return a}));const i={device:{"iPad4,1":"iPad Air","iPad5,1":"iPad mini 4","iPad6,3":"iPad Pro [9.7 in]","iPhone7,2":"iPhone 6","iPhone9,1":"iPhone 7"},device_type:{angler:"Nexus 6p",athene:"Moto G4",blueline:"Pixel 3",bullhead:"Nexus 5X",crosshatch:"Pixel 3 XL",darcy:"NVIDIA Shield [2017]",dragon:"Pixel C",flame:"Pixel 4",flo:"Nexus 7 [2013]",flounder:"Nexus 9",foster:"NVIDIA Shield [2015]",fugu:"Nexus Player",gce_x86:"Android on GCE",goyawifi:"Galaxy Tab 3",grouper:"Nexus 7 [2012]",hammerhead:"Nexus 5",herolte:"Galaxy S7 [Global]",heroqlteatt:"Galaxy S7 [AT&T]","iPad4,1":"iPad Air","iPad5,1":"iPad mini 4","iPad6,3":"iPad Pro [9.7 in]","iPhone7,2":"iPhone 6","iPhone9,1":"iPhone 7","iPhone10,1":"iPhone 8",j5xnlte:"Galaxy J5",m0:"Galaxy S3",mako:"Nexus 4",manta:"Nexus 10",marlin:"Pixel XL",sailfish:"Pixel",sargo:"Pixel 3a",shamu:"Nexus 6",sprout:"Android One",starlte:"Galaxy S9",taimen:"Pixel 2 XL","TECNO-KB8":"TECNO Spark 3 Pro",walleye:"Pixel 2",zerofltetmo:"Galaxy S6"},gpu:{1002:"AMD","1002:6613":"AMD Radeon R7 240","1002:6646":"AMD Radeon R9 M280X","1002:6779":"AMD Radeon HD 6450/7450/8450","1002:679e":"AMD Radeon HD 7800","1002:6821":"AMD Radeon HD 8870M","1002:683d":"AMD Radeon HD 7770/8760","1002:9830":"AMD Radeon HD 8400","1002:9874":"AMD Carrizo","1a03":"ASPEED","1a03:2000":"ASPEED Graphics Family","102b":"Matrox","102b:0522":"Matrox MGA G200e","102b:0532":"Matrox MGA G200eW","102b:0534":"Matrox G200eR2","10de":"NVIDIA","10de:08a4":"NVIDIA GeForce 320M","10de:08aa":"NVIDIA GeForce 320M","10de:0a65":"NVIDIA GeForce 210","10de:0fe9":"NVIDIA GeForce GT 750M Mac Edition","10de:0ffa":"NVIDIA Quadro K600","10de:104a":"NVIDIA GeForce GT 610","10de:11c0":"NVIDIA GeForce GTX 660","10de:1244":"NVIDIA GeForce GTX 550 Ti","10de:1401":"NVIDIA GeForce GTX 960","10de:1ba1":"NVIDIA GeForce GTX 1070","10de:1cb3":"NVIDIA Quadro P400","10de:2184":"NVIDIA GeForce GTX 1660",8086:"Intel","8086:0046":"Intel Ironlake HD Graphics","8086:0102":"Intel Sandy Bridge HD Graphics 2000","8086:0116":"Intel Sandy Bridge HD Graphics 3000","8086:0166":"Intel Ivy Bridge HD Graphics 4000","8086:0412":"Intel Haswell HD Graphics 4600","8086:041a":"Intel Haswell HD Graphics","8086:0a16":"Intel Haswell HD Graphics 4400","8086:0a26":"Intel Haswell HD Graphics 5000","8086:0a2e":"Intel Haswell Iris Graphics 5100","8086:0d26":"Intel Haswell Iris Pro Graphics 5200","8086:0f31":"Intel Bay Trail HD Graphics","8086:1616":"Intel Broadwell HD Graphics 5500","8086:161e":"Intel Broadwell HD Graphics 5300","8086:1626":"Intel Broadwell HD Graphics 6000","8086:162b":"Intel Broadwell Iris Graphics 6100","8086:1912":"Intel Skylake HD Graphics 530","8086:191e":"Intel Skylake HD Graphics 515","8086:1926":"Intel Skylake Iris 540/550","8086:193b":"Intel Skylake Iris Pro 580","8086:22b1":"Intel Braswell HD Graphics","8086:3e92":"Intel Coffee Lake UHD Graphics 630","8086:3ea5":"Intel Coffee Lake Iris Plus Graphics 655","8086:5912":"Intel Kaby Lake HD Graphics 630","8086:591e":"Intel Kaby Lake HD Graphics 615","8086:5926":"Intel Kaby Lake Iris Plus Graphics 640"},os:{"Windows-10-10240":"Windows 10 version 1507","Windows-10-10586":"Windows 10 version 1511","Windows-10-14393":"Windows 10 version 1607","Windows-10-15063":"Windows 10 version 1703","Windows-10-16299":"Windows 10 version 1709","Windows-10-17134":"Windows 10 version 1803","Windows-10-17763":"Windows 10 version 1809","Windows-10-18362":"Windows 10 version 1903","Windows-10-18363":"Windows 10 version 1909","Windows-Server-14393":"Windows Server 2016","Windows-Server-17134":"Windows Server version 1803","Windows-Server-17763":"Windows Server 2019 or version 1809","Windows-Server-18362":"Windows Server version 1903","Windows-Server-18363":"Windows Server version 1909"}},r=/.+\((.+)\)/;function o(t){return t?t.map(t=>{const e=t.split(":")[0];if(i[e]){const s=t.match(r);return s?e+":"+s[1]:t}return t}):[]}function a(t){const e=t.indexOf(":");if(e<0)return t;const s=t.substring(0,e),i=t.substring(e+1),r=s.split("-tag")[0];return`${s}:${n(i,r)}`}},,function(t,e,s){"use strict";s.d(e,"d",(function(){return n})),s.d(e,"b",(function(){return i})),s.d(e,"a",(function(){return r})),s.d(e,"c",(function(){return o}));const n=new Set(["PENDING","RUNNING"]),i=new Set(["TIMED_OUT","EXPIRED","NO_RESOURCE","CANCELED","KILLED"]),r=[{label:"Total",value:"..."},{label:"Success",value:"...",filter:"COMPLETED_SUCCESS"},{label:"Failure",value:"...",filter:"COMPLETED_FAILURE"},{label:"Pending",value:"...",filter:"PENDING"},{label:"Running",value:"...",filter:"RUNNING"},{label:"Timed Out",value:"...",filter:"TIMED_OUT"},{label:"Bot Died",value:"...",filter:"BOT_DIED"},{label:"Deduplicated",value:"...",filter:"DEDUPED"},{label:"Expired",value:"...",filter:"EXPIRED"},{label:"No Resource",value:"...",filter:"NO_RESOURCE"},{label:"Canceled",value:"...",filter:"CANCELED"},{label:"Killed",value:"...",filter:"KILLED"}],o=["ALL","COMPLETED","COMPLETED_SUCCESS","COMPLETED_FAILURE","RUNNING","PENDING","PENDING_RUNNING","BOT_DIED","DEDUPED","TIMED_OUT","EXPIRED","NO_RESOURCE","CANCELED","KILLED"]},function(t,e,s){"use strict";s.d(e,"a",(function(){return o}));var n=s(7),i=s(0),r=s(1);class o extends HTMLElement{constructor(t){super(),this._template=t,this._app=null,this._auth_header="",this._profile=null,this._notAuthorized=!1}connectedCallback(){Object(r.a)(this,"client_id"),Object(r.a)(this,"testing_offline"),this._authHeaderEvent=t=>{this._auth_header=t.detail.auth_header},this.addEventListener("log-in",this._authHeaderEvent)}disconnectedCallback(){this.removeEventListener("log-in",this._authHeaderEvent)}static get observedAttributes(){return["client_id","testing_offline"]}get app(){return this._app}get auth_header(){return this._auth_header}get loggedInAndAuthorized(){return!!this._auth_header&&!this._notAuthorized}get permissions(){return this._app&&this._app.permissions||{}}get profile(){return this._app&&this._app.profile||{}}get server_details(){return this._app&&this._app.server_details||{}}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}fetchError(t,e){403===t.status?(this._message="User unauthorized - try logging in with a different account",this._notAuthorized=!0,this.render()):"AbortError"!==t.name&&(console.error(t),Object(n.a)(`Unexpected error loading ${e}: ${t.message}`,5e3)),this._app.finishedTask()}render(){Object(i.d)(this._template(this),this,{eventContext:this}),this._app||(this._app=this.firstElementChild,Object(i.d)(this._template(this),this,{eventContext:this}))}attributeChangedCallback(t,e,s){this.render()}}},,function(t,e,s){"use strict";s.d(e,"a",(function(){return a}));var n=s(10);const i=t=>JSON.parse(JSON.stringify(t));function r(t,e){let s={};return Object.keys(t).forEach((function(i){(function(t,e){if(typeof t!=typeof e)return!1;let s=typeof t;return"string"===s||"boolean"===s||"number"===s?t===e:"object"===s?Array.isArray(s)?JSON.stringify(t)===JSON.stringify(e):Object(n.a)(t)===Object(n.a)(e):void 0})(t[i],e[i])||(s[i]=t[i])})),s}var o=s(6);function a(t,e){let s=i(t()),a=!1;const d=()=>{a=!0;let t=n.c(window.location.search.slice(1),s);e(function(t,e){let s={};return Object.keys(e).forEach((function(n){t.hasOwnProperty(n)?s[n]=i(t[n]):s[n]=i(e[n])})),s}(t,s))};return o.c.then(d),window.addEventListener("popstate",d),()=>{if(!a)return;let e=n.a(r(t(),s));history.pushState(null,"",window.location.origin+window.location.pathname+"?"+e)}}},function(t,e,s){"use strict";s(32)},function(t,e,s){},function(t,e,s){},function(t,e,s){},function(t,e,s){},function(t,e,s){"use strict";var n=s(7),i=s(0),r=s(17),o=s(9),a=s(1);window.customElements.define("toast-sk",class extends HTMLElement{constructor(){super(),this._timer=null}connectedCallback(){this.hasAttribute("duration")||(this.duration=5e3),Object(a.a)(this,"duration")}get duration(){return+this.getAttribute("duration")}set duration(t){this.setAttribute("duration",t)}show(){this.setAttribute("shown",""),this.duration>0&&!this._timer&&(this._timer=window.setTimeout(()=>{this._timer=null,this.hide()},this.duration))}hide(){this.removeAttribute("shown"),this._timer&&(window.clearTimeout(this._timer),this._timer=null)}});s(25);window.customElements.define("error-toast-sk",class extends HTMLElement{connectedCallback(){this.innerHTML="<toast-sk></toast-sk>",this._toast=this.firstElementChild,document.addEventListener("error-sk",this)}disconnectedCallback(){document.removeEventListener("error-sk",this)}handleEvent(t){t.detail.duration&&(this._toast.duration=t.detail.duration),this._toast.textContent=t.detail.message,this._toast.show()}});s(14);const d=document.createElement("template");d.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M20 8h-2.81c-.45-.78-1.07-1.45-1.82-1.96L17 4.41 15.59 3l-2.17 2.17C12.96 5.06 12.49 5 12 5c-.49 0-.96.06-1.41.17L8.41 3 7 4.41l1.62 1.63C7.88 6.55 7.26 7.22 6.81 8H4v2h2.09c-.05.33-.09.66-.09 1v1H4v2h2v1c0 .34.04.67.09 1H4v2h2.81c1.04 1.79 2.97 3 5.19 3s4.15-1.21 5.19-3H20v-2h-2.09c.05-.33.09-.66.09-1v-1h2v-2h-2v-1c0-.34-.04-.67-.09-1H20V8zm-6 8h-4v-2h4v2zm0-4h-4v-2h4v2z"/></svg>',window.customElements.define("bug-report-icon-sk",class extends HTMLElement{connectedCallback(){let t=d.content.cloneNode(!0);this.appendChild(t)}});const l=document.createElement("template");l.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>',window.customElements.define("menu-icon-sk",class extends HTMLElement{connectedCallback(){let t=l.content.cloneNode(!0);this.appendChild(t)}}),window.customElements.define("spinner-sk",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"active")}get active(){return this.hasAttribute("active")}set active(t){t?this.setAttribute("active",""):this.removeAttribute("active")}});s(26),s(27);const c=new Promise((t,e)=>{const s=()=>{void 0!==window.gapi?t():setTimeout(s,10)};setTimeout(s,10)});window.customElements.define("oauth-login",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._auth_header="",this.testing_offline?this._profile={email:"missing@chromium.org",imageURL:"http://storage.googleapis.com/gd-wagtail-prod-assets/original_images/logo_google_fonts_color_2x_web_64dp.png"}:(this._profile=null,c.then(()=>{gapi.load("auth2",()=>{gapi.auth2.init({client_id:this.client_id}).then(()=>{this._maybeFireLoginEvent(),this.render()},t=>{console.error(t),Object(n.a)(`Error initializing oauth: ${JSON.stringify(t)}`,1e4)})})})),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get auth_header(){return this._auth_header}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get profile(){return this._profile}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}_maybeFireLoginEvent(){const t=gapi.auth2.getAuthInstance().currentUser.get();if(t.isSignedIn()){const e=t.getBasicProfile();this._profile={email:e.getEmail(),imageURL:e.getImageUrl()};const s=t.getAuthResponse(!0),n=`${s.token_type} ${s.access_token}`;return this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:n,profile:this._profile},bubbles:!0})),this._auth_header=n,!0}return this._profile=null,this._auth_header="",!1}_logIn(){if(this.testing_offline)this._auth_header="Bearer 12345678910-boomshakalaka",this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:this._auth_header,profile:this._profile},bubbles:!0})),this.render();else{const t=gapi.auth2.getAuthInstance();t&&t.signIn({scope:"email",prompt:"select_account"}).then(()=>{this._maybeFireLoginEvent()||console.warn("login was not successful; maybe user canceled"),this.render()})}}_logOut(){if(this.testing_offline)this._auth_header="",this.render(),window.location.reload();else{const t=gapi.auth2.getAuthInstance();t&&t.signOut().then(()=>{this._auth_header="",this._profile=null,window.location.reload()})}}render(){var t;Object(i.d)((t=this).auth_header?i.c`
<div>
  <img class=center id=avatar src="${t._profile.imageURL}" width=30 height=30>
  <span class=center>${t._profile.email}</span>
  <span class=center>|</span>
  <a class=center @click=${t._logOut} href="#">Sign out</a>
</div>`:i.c`
<div>
  <a @click=${t._logIn} href="#">Sign in</a>
</div>`,this,{eventContext:this})}attributeChangedCallback(t,e,s){this.render()}});const h=document.createElement("template");h.innerHTML="\n<button class=toggle-button>\n  <menu-icon-sk>\n  </menu-icon-sk>\n</button>\n";const u=document.createElement("template");u.innerHTML="\n<div class=spinner-spacer>\n  <spinner-sk></spinner-sk>\n</div>\n";const _=document.createElement("template");_.innerHTML='\n<a target=_blank rel=noopener\n   href="https://bugs.chromium.org/p/chromium/issues/entry?components=Infra%3EPlatform%3ESwarming%3EWebUI&owner=kjlubick@chromium.org&status=Assigned">\n  <bug-report-icon-sk class=fab></bug-report-icon-sk>\n</a>',window.customElements.define("swarming-app",class extends HTMLElement{constructor(){super(),this._busyTaskCount=0,this._spinner=null,this._dynamicEle=null,this._auth_header="",this._profile={},this._server_details={server_version:"You must log in to see more details",bot_version:""},this._permissions={}}connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._addHTML(),this.addEventListener("log-in",t=>{this._auth_header=t.detail.auth_header,this._profile=t.detail.profile,this._fetch()}),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get busy(){return!!this._busyTaskCount}get permissions(){return this._permissions}get profile(){return this._profile}get server_details(){return this._server_details}get client_id(){return this.getAttribute("client_id")}set client_id(t){return this.setAttribute("client_id",t)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(t){t?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}addBusyTasks(t){this._busyTaskCount+=t,this._spinner&&this._busyTaskCount>0&&(this._spinner.active=!0)}finishedTask(){this._busyTaskCount--,this._busyTaskCount<=0&&(this._busyTaskCount=0,this._spinner&&(this._spinner.active=!1),this.dispatchEvent(new CustomEvent("busy-end",{bubbles:!0})))}_addHTML(){const t=this.querySelector("header"),e=t&&t.querySelector("aside"),s=this.querySelector("footer");if(!(t&&e&&e.classList.contains("hideable")))return;let n=h.content.cloneNode(!0);t.insertBefore(n,t.firstElementChild),n=t.firstElementChild,n.addEventListener("click",t=>this._toggleMenu(t,e));const i=u.content.cloneNode(!0);t.insertBefore(i,e),this._spinner=t.querySelector("spinner-sk");const r=document.createElement("span");r.classList.add("grow"),t.appendChild(r),this._dynamicEle=document.createElement("div"),this._dynamicEle.classList.add("right"),t.appendChild(this._dynamicEle);const o=document.createElement("error-toast-sk");s.append(o);const a=_.content.cloneNode(!0);s.append(a)}_toggleMenu(t,e){e.classList.toggle("shown")}_fetch(){if(!this._auth_header)return;this._server_details={server_version:"<loading>",bot_version:"<loading>"};const t={headers:{authorization:this._auth_header}};this.addBusyTasks(1),fetch("/_ah/api/swarming/v1/server/details",t).then(o.a).then(t=>{this._server_details=t,this.render(),this.dispatchEvent(new CustomEvent("server-details-loaded",{bubbles:!0})),this.finishedTask()}).catch(t=>{403===t.status?(this._server_details={server_version:"User unauthorized - try logging in with a different account",bot_version:""},this.render()):(console.error(t),Object(n.a)(`Unexpected error loading details: ${t.message}`,5e3)),this.finishedTask()}),this._fetchPermissions(t)}_fetchPermissions(t,e){this.addBusyTasks(1);let s="/_ah/api/swarming/v1/server/permissions";if(e){const t=new URLSearchParams;for(const[s,n]of Object.entries(e))t.append(s,n);s+=`?${t.toString()}`}fetch(s,t).then(o.a).then(t=>{this._permissions=t,this.render(),this.dispatchEvent(new CustomEvent("permissions-loaded",{bubbles:!0})),this.finishedTask()}).catch(t=>{403!==t.status&&(console.error(t),Object(n.a)(`Unexpected error loading permissions: ${t.message}`,5e3)),this.finishedTask()})}render(){var t;this._dynamicEle&&Object(i.d)((t=this,i.c`
<div class=server-version>
  Server:
  <a href=${Object(r.a)(function(t){if(t&&t.server_version){var e=t.server_version.split("-");if(2===e.length)return`https://chromium.googlesource.com/infra/luci/luci-py/+/${e[1]}`}}(t._server_details))}>
    ${t._server_details.server_version}
  </a>
</div>
<oauth-login client_id=${t.client_id}
             ?testing_offline=${t.testing_offline}>
</oauth-login>`),this._dynamicEle)}attributeChangedCallback(t,e,s){this.render()}});s(28)},function(t,e,s){"use strict";var n=s(1);class i extends HTMLElement{get _role(){return"checkbox"}static get observedAttributes(){return["checked","disabled","name","label"]}connectedCallback(){this.innerHTML=`<label><input type=${this._role}></input><span class=box></span><span class=label></span></label>`,this._label=this.querySelector(".label"),this._input=this.querySelector("input"),Object(n.a)(this,"checked"),Object(n.a)(this,"disabled"),Object(n.a)(this,"name"),Object(n.a)(this,"label"),this._input.checked=this.checked,this._input.disabled=this.disabled,this._input.setAttribute("name",this.getAttribute("name")),this._label.textContent=this.getAttribute("label")}get checked(){return this.hasAttribute("checked")}set checked(t){let e=!!t;this._input.checked=e,t?this.setAttribute("checked",""):this.removeAttribute("checked")}get disabled(){return this.hasAttribute("disabled")}set disabled(t){let e=!!t;this._input.disabled=e,e?this.setAttribute("disabled",""):this.removeAttribute("disabled")}get name(){return this._input.getAttribute("name")}set name(t){this.setAttribute("name",t),this._input.setAttribute("name",t)}get label(){return this._input.getAttribute("label")}set label(t){this.setAttribute("label",t),this._input.setAttribute("label",t)}attributeChangedCallback(t,e,s){if(!this._input)return;let n=null!=s;switch(t){case"checked":this._input.checked=n;break;case"disabled":this._input.disabled=n;break;case"name":this._input.name=s;break;case"label":this._label.textContent=s}}}window.customElements.define("checkbox-sk",i);s(31)},function(t,e,s){},function(t,e,s){},function(t,e,s){},function(t,e,s){"use strict";var n=s(6);const i=document.createElement("template");i.innerHTML="<div class=backdrop></div>",window.customElements.define("dialog-pop-over",class extends HTMLElement{constructor(){super(),this._backdrop=null,this._content=null}connectedCallback(){const t=i.content.cloneNode(!0);if(this.appendChild(t),this._backdrop=Object(n.b)(".backdrop",this),this._content=Object(n.b)(".content",this),!this._content)throw"You must have an element with class content to show."}hide(){this._backdrop.classList.remove("opened"),this._content.classList.remove("opened")}show(){const t=window.innerWidth,e=window.innerHeight,s=Math.min(this._content.offsetWidth,t-50),n=Math.min(this._content.offsetHeight,e-50);this._content.style.width=s,this._content.style.left=(t-s)/2,this._content.style.top=(e-n)/2,this._backdrop.classList.add("opened"),this._content.classList.add("opened")}});s(33)},,,function(t,e,s){},function(t,e,s){"use strict";var n=s(0),i=s(4);s(14);const r=document.createElement("template");r.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>',window.customElements.define("arrow-drop-down-icon-sk",class extends HTMLElement{connectedCallback(){let t=r.content.cloneNode(!0);this.appendChild(t)}});const o=document.createElement("template");o.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M7 14l5-5 5 5z"/></svg>',window.customElements.define("arrow-drop-up-icon-sk",class extends HTMLElement{connectedCallback(){let t=o.content.cloneNode(!0);this.appendChild(t)}});window.customElements.define("sort-toggle",class extends HTMLElement{constructor(){super()}connectedCallback(){Object(i.e)(this,"currentKey"),Object(i.e)(this,"key"),Object(i.e)(this,"direction"),this.addEventListener("click",()=>{this.toggle()}),this.render()}get currentKey(){return this._currentKey}set currentKey(t){this._currentKey=t,this.render()}get key(){return this._key}set key(t){this._key=t,this.render()}get direction(){return this._direction}set direction(t){this._direction=t,this.render()}toggle(){this.currentKey===this.key&&"asc"===this.direction?this.direction="desc":this.direction="asc",this.dispatchEvent(new CustomEvent("sort-change",{detail:{direction:this.direction,key:this.key},bubbles:!0}))}render(){var t;Object(n.d)((t=this,n.c`
<arrow-drop-down-icon-sk ?hidden=${t.key===t.currentKey&&"asc"===t.direction}>
</arrow-drop-down-icon-sk>
<arrow-drop-up-icon-sk ?hidden=${t.key===t.currentKey&&"desc"===t.direction}>
</arrow-drop-up-icon-sk>`),this,{eventContext:this})}});s(37)},function(t,e,s){"use strict";s(14);const n=document.createElement("template");n.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M13 7h-2v4H7v2h4v4h2v-4h4v-2h-4V7zm-1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>',window.customElements.define("add-circle-outline-icon-sk",class extends HTMLElement{connectedCallback(){let t=n.content.cloneNode(!0);this.appendChild(t)}})},function(t,e,s){"use strict";s(14);const n=document.createElement("template");n.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M7 11v2h10v-2H7zm5-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>',window.customElements.define("remove-circle-outline-icon-sk",class extends HTMLElement{connectedCallback(){let t=n.content.cloneNode(!0);this.appendChild(t)}})},,,,,,,,function(t,e,s){},function(t,e,s){},,,,,,,,,,function(t,e,s){"use strict";s.r(e);var n=s(6),i=s(7),r=s(0),o=s(17),a=s(9),d=s(23),l=(s(30),s(39),s(40),s(24),s(4));s(38);const c=t=>r.c`
<table>
  <thead>
    <tr>
      <th>
        <span>Name</span>
        <sort-toggle
            key=full_name
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Total</span>
        <sort-toggle
            key=total
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Success</span>
        <sort-toggle
            key=success
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Failed</span>
        <sort-toggle
            key=failed
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Died</span>
        <sort-toggle
            key=bot_died
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Average Duration</span>
        <sort-toggle
            key=avg_duration
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>
        <span>Average Overhead</span>
        <sort-toggle
            key=avg_overhead
            .currentKey=${t._sort}
            .direction=${t._dir}>
        </sort-toggle>
      </th>
      <th>Percent of Total</th>
    </tr>
  </thead>
  <tbody>
    ${t._sortAndLimitTasks().map(e=>((t,e)=>r.c`
<tr>
  <td title=${t.full_name} class=break-all>${e._shortenName(t.full_name)}</td>
  <td>${t.total}</td>
  <td>${t.success}</td>
  <td>${t.failed}</td>
  <td>${t.bot_died}</td>
  <td>${Object(l.d)(t.avg_duration)}</td>
  <td>${Object(l.d)(t.avg_overhead)}</td>
  <td>${t.total_time_percent}%</td>
</tr>
`)(e,t))}

    <tr class=thick>
      <td>Total</td>
      <td>${t._totalStats.total}</td>
      <td>${t._totalStats.success}</td>
      <td>${t._totalStats.failed}</td>
      <td>${t._totalStats.bot_died}</td>
      <td>${Object(l.d)(t._totalStats.avg_duration)}</td>
      <td>${Object(l.d)(t._totalStats.avg_overhead)}</td>
      <td>100.0%</td>
    </tr>
  </tbody>
</table>

<div>
  <table>
    <thead>
      <tr>
        <th title="How much time passed between the oldest task fetched and now.">
          Total Wall Time
        </th>
        <th title="How much of the wall time this bot was busy with a task.">
          Wall Time Utilization
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>${Object(l.d)(t._totalStats.wall_time)}</td>
        <td>${t._totalStats.wall_time_utilization}%</td>
      </tr>
    </tbody>
  </table>

  <div class=controls>
    <checkbox-sk
        ?checked=${t._fullNames}
        @click=${t._toggleName}>
    </checkbox-sk>
    <span>Show Full Names</span>

    <checkbox-sk
        ?hidden=${t._summarized.length<=15}
        ?checked=${t._showAllTasks}
        @click=${t._toggleShow}>
    </checkbox-sk>
    <span ?hidden=${t._summarized.length<=15}>Show All Tasks</span>
  </div>
</div>
`;function h(t){return t=(t=(t=function(t){const e=t.split("/");return 5===e.length&&(t=e[0]+"/"+e[3]),t=t.replace(" (with patch)","")}(t=t.trim())).replace(/ \(retry\)/g,"")).replace(/ \(debug\)/g,"")}window.customElements.define("bot-page-summary",class extends HTMLElement{constructor(){super(),this._sort="total",this._dir="desc",this._summarized=[],this._totalStats={},this._showAllTasks=!1,this._fullNames=!1}connectedCallback(){Object(l.e)(this,"tasks"),this._sortEvent=t=>{this._sort=t.detail.key,this._dir=t.detail.direction,this.render()},this.addEventListener("sort-change",this._sortEvent)}disconnectedCallback(){this.removeEventListener("sort-change",this._sortEvent)}get tasks(){return this._tasks||[]}set tasks(t){this._tasks=t,this.render()}_aggregate(){const t={total:0,success:0,failed:0,bot_died:0,avg_duration:0,avg_overhead:0,total_overhead:0,total_time:0};if(!this.tasks||!this.tasks.length)return this._totalStats=t,void(this._summarized=[]);const e=new Date,s={};t.wall_time=(e-this.tasks[this.tasks.length-1].started_ts)/1e3;for(const e of this.tasks){const n=h(e.name);if("RUNNING"===e.state)continue;s[n]||(s[n]={full_name:n,total:0,success:0,failed:0,bot_died:0,avg_duration:0,total_time:0,total_overhead:0}),t.total++,s[n].total++,e.failure?(t.failed++,s[n].failed++):e.internal_failure&&(t.bot_died++,s[n].bot_died++);const i=e.total_duration||e.duration||0;t.total_time+=i,s[n].total_time+=i,t.total_overhead+=e.total_overhead||0,s[n].total_overhead+=e.total_overhead||0}const n=[];for(const e in s){const i=s[e];i.avg_duration=i.total_time/i.total,i.avg_overhead=i.total_overhead/i.total,i.total_time_percent=(100*i.total_time/t.total_time).toFixed(1),n.push(i)}t.avg_duration=t.total_time/t.total,t.avg_overhead=t.total_overhead/t.total,t.wall_time_utilization=(100*t.total_time/t.wall_time).toFixed(1),this._totalStats=t,this._summarized=n}render(){this._aggregate(),Object(r.d)(c(this),this,{eventContext:this})}_sortAndLimitTasks(){return this._summarized.sort((t,e)=>{if(!this._sort)return 0;let s=1;return"desc"===this._dir&&(s=-1),"full_name"===this._sort?s*t.full_name.localeCompare(e.full_name):s*(t[this._sort]-e[this._sort])}),this._showAllTasks?this._summarized:this._summarized.slice(0,Math.min(this._summarized.length,15))}_shortenName(t){return t.length>50&&!this._fullNames?t.slice(0,47)+"...":t}_toggleName(t){t.preventDefault(),this._fullNames=!this._fullNames,this.render()}_toggleShow(t){t.preventDefault(),this._showAllTasks=!this._showAllTasks,this.render()}});s(48),s(34),s(29);var u=s(18);function _(t){if(!t)return[];for(const e of t)Object(l.h)(e,"ts");return t.sort((t,e)=>e.ts-t.ts),t}function p(t){if(!t)return[];for(const e of t){for(const t of b)Object(l.h)(e,t);if(e.duration)e.human_duration=Object(l.d)(e.duration);else{const t=e.completed_ts||e.abandoned_ts||e.modified_ts||new Date;e.human_duration=Object(l.l)(e.started_ts,t),e.duration=(t.getTime()-e.started_ts)/1e3}const t=e.performance_stats&&e.performance_stats.bot_overhead||0;e.total_duration=e.duration+t,e.human_total_duration=Object(l.d)(e.total_duration),e.total_overhead=t,e.human_state=e.state||"UNKNOWN","COMPLETED"===e.state&&(e.failure?e.human_state="FAILURE":"RUNNING"!==e.state&&(e.human_state="SUCCESS"))}return t.sort((t,e)=>e.started_ts-t.started_ts),t}const f=["id","caches","server_version"];const m=["first_seen_ts","last_seen_ts","lease_expiration_ts"],b=["started_ts","completed_ts","abandoned_ts","modified_ts"],g=["include_performance_stats=true","limit=30","sort=STARTED_TS",encodeURIComponent("fields=cursor,items(state,bot_version,completed_ts,created_ts,duration,exit_code,failure,internal_failure,modified_ts,name,server_versions,started_ts,task_id)")].join("&"),v="limit=50&fields=cursor%2Citems(event_type%2Cmaintenance_msg%2Cmessage%2Cquarantined%2Ctask_id%2Cts%2Cversion)";var k=s(15),w=s(21);const E=t=>r.c`
<tr>
  <td rowspan=${t.length+1}>
    <a href=${function(t){const e=["id","os","task","status"];if(!t)return Object(l.a)([],e);t=t.filter(t=>-1===f.indexOf(t.key));for(const s of t)-1===e.indexOf(s.key)&&e.push(s.key);return Object(l.a)(t,e)}(t)}>
      Dimensions
    </a>
  </td>
</tr>
${t.map(y)}
`,y=t=>r.c`
<tr>
  <td>${t.key}</td>
  <td>${t.value.join(" | ")}</td>
</tr>
`,$=t=>r.c`
<tr>
  <td>${t.id}</td>
  <td>${t.battery&&t.battery.level||"???"}</td>
  <td>${t.averageTemp}</td>
  <td>${t.state}</td>
</tr>
`,T=t=>r.c`
<tr class=${Object(k.m)(t)}>
  <td class=break-all>
    <a target=_blank rel=noopener
        href=${Object(l.j)(t.task_id)}>
      ${t.name}
    </a>
  </td>
  <td>${t.human_started_ts}</td>
  <td title=${t.human_completed_ts}>${t.human_total_duration}</td>
  <td>${t.human_state}</td>
</tr>
`,x=(t,e,s)=>e||t.message?r.c`
<tr>
  <td class=message>${t.message}</td>
  <td>${t.event_type}</td>
  <td>${t.human_ts}</td>
  <td>
    <a target=_blank rel=noopener
        href=${Object(l.j)(t.task_id)}>
      ${t.task_id}
    </a>
  </td>
  <td class=${s===t.version?"":"old_version"}>
      ${t.version&&t.version.substring(0,10)}
  </td>
</tr>`:"",C=t=>{return r.c`
<swarming-app id=swapp
              client_id=${t.client_id}
              ?testing_offline=${t.testing_offline}>
  <header>
    <div class=title>Swarming Bot Page</div>
      <aside class=hideable>
        <a href=/>Home</a>
        <a href=/botlist>Bot List</a>
        <a href=/tasklist>Task List</a>
        <a href=/task>Task Page</a>
      </aside>
  </header>
  <main>
    <h2 class=message ?hidden=${t.loggedInAndAuthorized}>${t._message}</h2>

    <div class=top ?hidden=${!t.loggedInAndAuthorized}>
      ${(t=>t._botId?r.c`
<div class=id_buttons>
  <input id=id_input placeholder="Bot ID" @change=${t._updateID}></input>
  <button title="Refresh data" class=refresh
          @click=${t._refresh}>refresh</button>
</div>`:r.c`
<div class=id_buttons>
  <input id=id_input placeholder="Bot ID" @change=${t._updateID}></input>
  <span class=message>Enter a Bot ID to get started.</span>
</div>`)(t)}
      <h2 class=not_found ?hidden=${!t._notFound||!t._botId}>
        Bot not found
      </h2>
    </div>
    <div class="horizontal layout wrap content"
         ?hidden=${!t.loggedInAndAuthorized||!t._botId||t._notFound}>
      <div class=grow>
        <table class=data_table>
          ${((t,e)=>t._botId?r.c`
<tr class="dead ${e.deleted?"":"hidden"}"
    title="This bot was deleted.">
  <td colspan=3>THIS BOT WAS DELETED</td>
</tr>
<tr class=${e.is_dead?"dead":""}>
  <td>Last Seen</td>
  <td title=${e.human_last_seen_ts}>${Object(l.l)(e.last_seen_ts)} ago</td>
  <td>
    <button class='shut_down ${!e.is_dead&&e.first_seen_ts?"":"hidden"}'
          ?hidden=${e.is_dead}
          ?disabled=${!t.permissions.terminate_bot}
          @click=${t._promptShutdown}>
      Stop the bot gracefully
    </button>
    <button class='delete ${e.is_dead&&!e.deleted?"":"hidden"}'
          ?disabled=${!t.permissions.delete_bot}
          @click=${t._promptDelete}>
      Delete
    </button>
  </td>
</tr>
<tr class="quarantined ${e.quarantined?"":"hidden"}">
  <td>Quarantined</td>
  <td colspan=2 class=code>
    ${function(t){if(t&&t.quarantined){let e=t.state.quarantined;return void 0!==e&&"true"!==e&&!0!==e||(e=t.state&&t.state.error),e||"True"}return""}(e)}
  </td>
</tr>
<tr class="dead ${e.is_dead&&!e.deleted?"":"hidden"}">
  <td>Dead</td>
  <td colspan=2 class=code>Bot has been missing longer than 10 minutes</td>
</tr>
<tr class="maintenance ${e.maintenance_msg?"":"hidden"}">
  <td>In Maintenance</td>
  <td colspan=2 class=code>${e.maintenance_msg}</td>
</tr>
<tr>
  <td>${e.is_dead?"Died on Task":"Current Task"}</td>
  <td>
    <a target=_blank rel=noopener
        href=${Object(o.a)(Object(l.j)(e.task_id))}>
      ${e.task_id||"idle"}
    </a>
  </td>
  <td>
    <button class=kill
            ?hidden=${!e.task_id||e.is_dead}
            ?disabled=${!t.permissions.cancel_task}
            @click=${t._promptKill}>
        Kill task
      </button>
  </td>
</tr>`:"")(t,t._bot)}
          ${E(t._bot.dimensions||[])}
          ${((t,e)=>r.c`
<tr title="IP address that the server saw the connection from.">
  <td>External IP</td>
  <td colspan=2><a href=${"http://"+e.external_ip}>${e.external_ip}</a></td>
</tr>
<tr class=${t.server_details.bot_version===e.version?"":"old_version"}
    title="Version is based on the content of swarming_bot.zip which is the swarming bot code.
           The bot won't update if quarantined, dead, or busy.">
  <td>Bot Version</td>
  <td colspan=2>${e.version&&e.version.substring(0,10)}</td>
</tr>
<tr title="The version the server expects the bot to be using.">
  <td>Expected Bot Version</td>
  <td colspan=2>${t.server_details.bot_version&&t.server_details.bot_version.substring(0,10)}</td>
</tr>
<tr title="First time ever a bot with this id contacted the server.">
  <td>First seen</td>
  <td colspan=2 title=${e.human_first_seen_ts}>
    ${Object(l.k)(e.first_seen_ts)} ago
  </td>
</tr>
<tr title="How the bot is authenticated by the server.">
  <td>Authenticated as</td>
  <td colspan=2>${e.authenticated_as}</td>
</tr>
<tr ?hidden=${!e.lease_id}>
  <td>Machine Provider Lease ID</td>
  <td colspan=2>
    <a href=${Object(o.a)(function(t,e){const s=e.machine_provider_template;if(t.lease_id&&s)return s.replace("%s",t.lease_id)}(e,t.server_details))}>
      ${e.lease_id}
    </a>
  </td>
</tr>
<tr ?hidden=${!e.lease_id}>
  <td>Machine Provider Lease Expires</td>
  <td colspan=2>${e.human_lease_expiration_ts}</td>
</tr>
`)(t,t._bot)}
        </table>
        ${e=t._bot,e.device_list&&e.device_list.length?r.c`
<h2>Android Devices</h2>

<table class=devices>
  <thead>
    <tr>
      <th>ID</th>
      <th>Battery</th>
      <th>Avg Temp. (°C)</th>
      <th>State</th>
    </tr>
  </thead>
  <tbody>
    ${e.device_list.map($)}
  </tbody>
</table>`:""}
        ${((t,e)=>r.c`
<span class=title>State</span>
<button class=state @click=${t._toggleBotState}>
  <add-circle-outline-icon-sk ?hidden=${t._showState}></add-circle-outline-icon-sk>
  <remove-circle-outline-icon-sk ?hidden=${!t._showState}></remove-circle-outline-icon-sk>
</button>

<div ?hidden=${!t._showState} class=bot_state>
  ${JSON.stringify(e&&e.state||{},null,2)}
</div>
`)(t,t._bot)}
      </div>

      <div class="stats grow">
        <bot-page-summary .tasks=${t._tasks}></bot-page-summary>
      </div>
    </div>

    <div class=tasks-events-picker
         ?hidden=${!t.loggedInAndAuthorized||!t._botId||t._notFound}>
      <div class=tab
           @click=${e=>t._setShowEvents(!1)}
           ?selected=${!t._showEvents}>
        Tasks
      </div>
      <div class=tab
           @click=${e=>t._setShowEvents(!0)}
           ?selected=${t._showEvents}>
        Events
      </div>
    </div>

    ${((t,e)=>!t.loggedInAndAuthorized||!t._botId||t._showEvents||t._notFound?"":r.c`
<table class=tasks_table>
  <thead>
    <tr>
      <th>Task</th>
      <th>Started</th>
      <th>Duration</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    ${e.map(T)}
  </tbody>
</table>

<button class=more_tasks
        ?disabled=${!t._taskCursor}
        @click=${t._moreTasks}>
  Show More
</button>
`)(t,t._tasks)}
    ${((t,e)=>t.loggedInAndAuthorized&&t._botId&&t._showEvents&&!t._notFound?r.c`
<div class=all-events>
  <checkbox-sk ?checked=${t._showAll}
               @click=${t._toggleShowAll}>
  </checkbox-sk>
  <span>Show all events</span>
</div>
<table class=events_table>
  <thead>
    <tr>
      <th>Message</th>
      <th>Type</th>
      <th>Timestamp</th>
      <th>Task ID</th>
      <th>Version</th>
    </tr>
  </thead>
  <tbody>
    ${e.map(e=>x(e,t._showAll,t.server_details.bot_version))}
  </tbody>
</table>

<button class=more_events
        ?disabled=${!t._eventsCursor}
        @click=${t._moreEvents}>
  Show More
</button>
`:"")(t,t._events)}

  </main>
  <footer></footer>
  <dialog-pop-over>
    <div class='prompt-dialog content'>
      Are you sure you want to ${t._prompt}?
      <div class="horizontal layout end">
        <button @click=${t._closePopup} class=cancel tabindex=0>NO</button>
        <button @click=${t._promptCallback} class=ok tabindex=0>YES</button>
      </div>
    </div>
  </dialog-pop-over>
</swarming-app>
`;var e};window.customElements.define("bot-page",class extends w.a{constructor(){super(C),this._botId="",this._showState=!1,this._showEvents=!1,this._showAll=!1,this._urlParamsLoaded=!1,this._stateChanged=Object(d.a)(()=>({id:this._botId,s:this._showState,e:this._showEvents,a:this._showAll}),t=>{this._botId=t.id||this._botId,this._showState=t.s,this._showEvents=t.e,this._showAll=t.a,this._urlParamsLoaded=!0,this._fetch(),this.render()}),this._bot={},this._notFound=!1,this._tasks=[],this._events=[],this._resetCursors(),this._promptCallback=()=>{},this._message="You must sign in to see anything useful.",this._fetchController=null}connectedCallback(){super.connectedCallback(),this._loginEvent=t=>{this._fetch(),this.render()},this.addEventListener("log-in",this._loginEvent),this.render()}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("log-in",this._loginEvent)}_closePopup(){Object(n.b)("dialog-pop-over",this).hide()}_deleteBot(){this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/delete`,{method:"POST",headers:{authorization:this.auth_header,"content-type":"application/json; charset=UTF-8"}}).then(a.a).then(t=>{this._closePopup(),Object(i.a)("Request to delete bot sent",4e3),this.render(),this.app.finishedTask()}).catch(t=>{this._closePopup(),this.fetchError(t,"bot/delete"),this.render()})}_fetch(){if(!this.loggedInAndAuthorized||!this._urlParamsLoaded||!this._botId)return;this._fetchController&&this._fetchController.abort(),this._fetchController=new AbortController;const t={headers:{authorization:this.auth_header},signal:this._fetchController.signal};this.app._fetchPermissions(t,{bot_id:this._botId}),this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/get`,t).then(a.a).then(t=>{this._notFound=!1,this._bot=function(t){if(!t)return{};t.state=t.state||"{}",t.state=JSON.parse(t.state)||{},t.dimensions=t.dimensions||[];for(const e of t.dimensions)e.value.forEach((function(t,s){e.value[s]=Object(u.a)(t,e.key)}));t.device_list=[];const e=t.state.devices;if(e)for(const s in e)if(e.hasOwnProperty(s)){const n=e[s];n.id=s,t.device_list.push(n);let i=0,r=0;n.temp=n.temp||{};for(const t in n.temp)r+=parseFloat(n.temp[t]),i++;n.averageTemp=i?(r/i).toFixed(1):"???"}for(const e of m)Object(l.h)(t,e);return t}(t),this.render(),this.app.finishedTask()}).catch(t=>{404===t.status&&(this._bot={},this._notFound=!0,this.render()),this.fetchError(t,"bot/data")}),this._taskCursor||(this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/tasks?${g}`,t).then(a.a).then(t=>{this._taskCursor=t.cursor,this._tasks=p(t.items),this.render(),this.app.finishedTask()}).catch(t=>this.fetchError(t,"bot/tasks"))),this._eventsCursor||(this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/events?${v}`,t).then(a.a).then(t=>{this._eventsCursor=t.cursor,this._events=_(t.items),this.render(),this.app.finishedTask()}).catch(t=>this.fetchError(t,"bot/events")))}_killTask(){this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/task/${this._bot.task_id}/cancel`,{method:"POST",headers:{authorization:this.auth_header,"content-type":"application/json"},body:JSON.stringify({kill_running:!0})}).then(a.a).then(t=>{this._closePopup(),Object(i.a)("Request to kill task sent",4e3),this.render(),this.app.finishedTask()}).catch(t=>{this._closePopup(),this.fetchError(t,"task/kill"),this.render()})}_moreEvents(){if(!this._eventsCursor)return;const t={headers:{authorization:this.auth_header},signal:this._fetchController.signal};this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/events?cursor=${this._eventsCursor}&`+v,t).then(a.a).then(t=>{this._eventsCursor=t.cursor,this._events.push(..._(t.items)),this.render(),this.app.finishedTask()}).catch(t=>this.fetchError(t,"bot/more_events"))}_moreTasks(){if(!this._taskCursor)return;const t={headers:{authorization:this.auth_header},signal:this._fetchController.signal};this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/tasks?cursor=${this._taskCursor}&`+g,t).then(a.a).then(t=>{this._taskCursor=t.cursor,this._tasks.push(...p(t.items)),this.render(),this.app.finishedTask()}).catch(t=>this.fetchError(t,"bot/more_tasks"))}_promptDelete(){this._prompt=`delete dead bot '${this._botId}'`,this._promptCallback=this._deleteBot,this.render(),Object(n.b)("dialog-pop-over",this).show(),Object(n.b)("dialog-pop-over button.cancel",this).focus()}_promptKill(){this._prompt=`kill running task '${this._bot.task_id}'`,this._promptCallback=this._killTask,this.render(),Object(n.b)("dialog-pop-over",this).show(),Object(n.b)("dialog-pop-over button.cancel",this).focus()}_promptShutdown(){this._prompt=`gracefully shut down bot '${this._botId}'`,this._promptCallback=this._shutdownBot,this.render(),Object(n.b)("dialog-pop-over",this).show(),Object(n.b)("dialog-pop-over button.cancel",this).focus()}_refresh(){this._resetCursors(),this._fetch(),this.render()}render(){super.render(),Object(n.b)("#id_input",this).value=this._botId}_resetCursors(){this._taskCursor="",this._eventsCursor=""}_setShowEvents(t){this._showEvents=t,this._stateChanged(),this.render()}_shutdownBot(){this.app.addBusyTasks(1),fetch(`/_ah/api/swarming/v1/bot/${this._botId}/terminate`,{method:"POST",headers:{authorization:this.auth_header,"content-type":"application/json"}}).then(a.a).then(t=>{this._closePopup(),Object(i.a)("Request to shutdown bot sent",4e3),this.render(),this.app.finishedTask()}).catch(t=>{this._closePopup(),this.fetchError(t,"bot/terminate"),this.render()})}_toggleBotState(t){this._showState=!this._showState,this._stateChanged(),this.render()}_toggleShowAll(t){t.preventDefault(),this._showAll=!this._showAll,this._stateChanged(),this.render()}_updateID(t){const e=Object(n.b)("#id_input",this);this._botId=e.value,this._resetCursors(),this._stateChanged(),this._fetch(),this.render()}});s(49)}]);