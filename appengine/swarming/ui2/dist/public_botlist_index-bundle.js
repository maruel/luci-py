!function(e){var t={};function s(i){if(t[i])return t[i].exports;var n=t[i]={i:i,l:!1,exports:{}};return e[i].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=t,s.d=function(e,t,i){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},s.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(s.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)s.d(i,n,function(t){return e[t]}.bind(null,n));return i},s.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/newres/",s(s.s=60)}([function(e,t,s){"use strict";s.d(t,"b",(function(){return o.a})),s.d(t,"a",(function(){return i.b})),s.d(t,"d",(function(){return u})),s.d(t,"c",(function(){return f}));var i=s(3);
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
 */const n=new class{handleAttributeExpressions(e,t,s,n){const r=t[0];if("."===r){return new i.f(e,t.slice(1),s).parts}return"@"===r?[new i.d(e,t.slice(1),n.eventContext)]:"?"===r?[new i.c(e,t.slice(1),s)]:new i.a(e,t,s).parts}handleTextExpression(e){return new i.e(e)}};var r=s(12),o=s(11),a=s(8),l=(s(5),s(2));
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
function c(e){let t=d.get(e.type);void 0===t&&(t={stringsArray:new WeakMap,keyString:new Map},d.set(e.type,t));let s=t.stringsArray.get(e.strings);if(void 0!==s)return s;const i=e.strings.join(l.f);return s=t.keyString.get(i),void 0===s&&(s=new l.a(e,e.getTemplateElement()),t.keyString.set(i,s)),t.stringsArray.set(e.strings,s),s}const d=new Map,h=new WeakMap,u=(e,t,s)=>{let n=h.get(t);void 0===n&&(Object(a.b)(t,t.firstChild),h.set(t,n=new i.e(Object.assign({templateFactory:c},s))),n.appendInto(t)),n.setValue(e),n.commit()};
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
 */(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.0.0");const f=(e,...t)=>new r.b(e,t,"html",n)},function(e,t,s){"use strict";function i(e,t){if(e.hasOwnProperty(t)){let s=e[t];delete e[t],e[t]=s}}s.d(t,"a",(function(){return i}))},function(e,t,s){"use strict";s.d(t,"f",(function(){return i})),s.d(t,"g",(function(){return n})),s.d(t,"b",(function(){return o})),s.d(t,"a",(function(){return a})),s.d(t,"d",(function(){return l})),s.d(t,"c",(function(){return c})),s.d(t,"e",(function(){return d}));
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
const i=`{{lit-${String(Math.random()).slice(2)}}}`,n=`\x3c!--${i}--\x3e`,r=new RegExp(`${i}|${n}`),o="$lit$";class a{constructor(e,t){this.parts=[],this.element=t;let s=-1,n=0;const a=[],l=t=>{const h=t.content,u=document.createTreeWalker(h,133,null,!1);let f=0;for(;u.nextNode();){s++;const t=u.currentNode;if(1===t.nodeType){if(t.hasAttributes()){const a=t.attributes;let l=0;for(let e=0;e<a.length;e++)a[e].value.indexOf(i)>=0&&l++;for(;l-- >0;){const i=e.strings[n],a=d.exec(i)[2],l=a.toLowerCase()+o,c=t.getAttribute(l).split(r);this.parts.push({type:"attribute",index:s,name:a,strings:c}),t.removeAttribute(l),n+=c.length-1}}"TEMPLATE"===t.tagName&&l(t)}else if(3===t.nodeType){const e=t.data;if(e.indexOf(i)>=0){const i=t.parentNode,o=e.split(r),l=o.length-1;for(let e=0;e<l;e++)i.insertBefore(""===o[e]?c():document.createTextNode(o[e]),t),this.parts.push({type:"node",index:++s});""===o[l]?(i.insertBefore(c(),t),a.push(t)):t.data=o[l],n+=l}}else if(8===t.nodeType)if(t.data===i){const e=t.parentNode;null!==t.previousSibling&&s!==f||(s++,e.insertBefore(c(),t)),f=s,this.parts.push({type:"node",index:s}),null===t.nextSibling?t.data="":(a.push(t),s--),n++}else{let e=-1;for(;-1!==(e=t.data.indexOf(i,e+1));)this.parts.push({type:"node",index:-1})}}};l(t);for(const e of a)e.parentNode.removeChild(e)}}const l=e=>-1!==e.index,c=()=>document.createComment(""),d=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F \x09\x0a\x0c\x0d"'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/},function(e,t,s){"use strict";s.d(t,"g",(function(){return c})),s.d(t,"a",(function(){return d})),s.d(t,"b",(function(){return h})),s.d(t,"e",(function(){return u})),s.d(t,"c",(function(){return f})),s.d(t,"f",(function(){return p})),s.d(t,"d",(function(){return b}));var i=s(11),n=s(8),r=s(5),o=s(16),a=s(12),l=s(2);
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
const c=e=>null===e||!("object"==typeof e||"function"==typeof e);class d{constructor(e,t,s){this.dirty=!0,this.element=e,this.name=t,this.strings=s,this.parts=[];for(let e=0;e<s.length-1;e++)this.parts[e]=this._createPart()}_createPart(){return new h(this)}_getValue(){const e=this.strings,t=e.length-1;let s="";for(let i=0;i<t;i++){s+=e[i];const t=this.parts[i];if(void 0!==t){const e=t.value;if(null!=e&&(Array.isArray(e)||"string"!=typeof e&&e[Symbol.iterator]))for(const t of e)s+="string"==typeof t?t:String(t);else s+="string"==typeof e?e:String(e)}}return s+=e[t],s}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class h{constructor(e){this.value=void 0,this.committer=e}setValue(e){e===r.a||c(e)&&e===this.value||(this.value=e,Object(i.b)(e)||(this.committer.dirty=!0))}commit(){for(;Object(i.b)(this.value);){const e=this.value;this.value=r.a,e(this)}this.value!==r.a&&this.committer.commit()}}class u{constructor(e){this.value=void 0,this._pendingValue=void 0,this.options=e}appendInto(e){this.startNode=e.appendChild(Object(l.c)()),this.endNode=e.appendChild(Object(l.c)())}insertAfterNode(e){this.startNode=e,this.endNode=e.nextSibling}appendIntoPart(e){e._insert(this.startNode=Object(l.c)()),e._insert(this.endNode=Object(l.c)())}insertAfterPart(e){e._insert(this.startNode=Object(l.c)()),this.endNode=e.endNode,e.endNode=this.startNode}setValue(e){this._pendingValue=e}commit(){for(;Object(i.b)(this._pendingValue);){const e=this._pendingValue;this._pendingValue=r.a,e(this)}const e=this._pendingValue;e!==r.a&&(c(e)?e!==this.value&&this._commitText(e):e instanceof a.b?this._commitTemplateResult(e):e instanceof Node?this._commitNode(e):Array.isArray(e)||e[Symbol.iterator]?this._commitIterable(e):e===r.b?(this.value=r.b,this.clear()):this._commitText(e))}_insert(e){this.endNode.parentNode.insertBefore(e,this.endNode)}_commitNode(e){this.value!==e&&(this.clear(),this._insert(e),this.value=e)}_commitText(e){const t=this.startNode.nextSibling;e=null==e?"":e,t===this.endNode.previousSibling&&3===t.nodeType?t.data=e:this._commitNode(document.createTextNode("string"==typeof e?e:String(e))),this.value=e}_commitTemplateResult(e){const t=this.options.templateFactory(e);if(this.value instanceof o.a&&this.value.template===t)this.value.update(e.values);else{const s=new o.a(t,e.processor,this.options),i=s._clone();s.update(e.values),this._commitNode(i),this.value=s}}_commitIterable(e){Array.isArray(this.value)||(this.value=[],this.clear());const t=this.value;let s,i=0;for(const n of e)s=t[i],void 0===s&&(s=new u(this.options),t.push(s),0===i?s.appendIntoPart(this):s.insertAfterPart(t[i-1])),s.setValue(n),s.commit(),i++;i<t.length&&(t.length=i,this.clear(s&&s.endNode))}clear(e=this.startNode){Object(n.b)(this.startNode.parentNode,e.nextSibling,this.endNode)}}class f{constructor(e,t,s){if(this.value=void 0,this._pendingValue=void 0,2!==s.length||""!==s[0]||""!==s[1])throw new Error("Boolean attributes can only contain a single expression");this.element=e,this.name=t,this.strings=s}setValue(e){this._pendingValue=e}commit(){for(;Object(i.b)(this._pendingValue);){const e=this._pendingValue;this._pendingValue=r.a,e(this)}if(this._pendingValue===r.a)return;const e=!!this._pendingValue;this.value!==e&&(e?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)),this.value=e,this._pendingValue=r.a}}class p extends d{constructor(e,t,s){super(e,t,s),this.single=2===s.length&&""===s[0]&&""===s[1]}_createPart(){return new _(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class _ extends h{}let m=!1;try{const e={get capture(){return m=!0,!1}};window.addEventListener("test",e,e),window.removeEventListener("test",e,e)}catch(e){}class b{constructor(e,t,s){this.value=void 0,this._pendingValue=void 0,this.element=e,this.eventName=t,this.eventContext=s,this._boundHandleEvent=e=>this.handleEvent(e)}setValue(e){this._pendingValue=e}commit(){for(;Object(i.b)(this._pendingValue);){const e=this._pendingValue;this._pendingValue=r.a,e(this)}if(this._pendingValue===r.a)return;const e=this._pendingValue,t=this.value,s=null==e||null!=t&&(e.capture!==t.capture||e.once!==t.once||e.passive!==t.passive),n=null!=e&&(null==t||s);s&&this.element.removeEventListener(this.eventName,this._boundHandleEvent,this._options),n&&(this._options=g(e),this.element.addEventListener(this.eventName,this._boundHandleEvent,this._options)),this.value=e,this._pendingValue=r.a}handleEvent(e){"function"==typeof this.value?this.value.call(this.eventContext||this.element,e):this.value.handleEvent(e)}}const g=e=>e&&(m?{capture:e.capture,passive:e.passive,once:e.once}:e.capture)},function(e,t,s){"use strict";s.d(t,"b",(function(){return o})),s.d(t,"a",(function(){return a})),s.d(t,"c",(function(){return l})),s.d(t,"d",(function(){return c})),s.d(t,"e",(function(){return d})),s.d(t,"f",(function(){return h})),s.d(t,"g",(function(){return u})),s.d(t,"h",(function(){return f})),s.d(t,"i",(function(){return p})),s.d(t,"j",(function(){return _})),s.d(t,"k",(function(){return m})),s.d(t,"l",(function(){return b}));var i=s(13),n=s(10),r=s(1);function o(e){if(e)return"/bot?id="+e}function a(e=[],t=[]){const s=[];for(const t of e)if(t.key&&t.value)if(Array.isArray(t.value))for(const e of t.value)s.push(t.key+":"+e);else s.push(t.key+":"+t.value);else s.push(t);const i={f:s,c:t};return"/botlist?"+n.b(i)}function l(e){return e||(e=[]),function(t,s){let i=e.indexOf(t);-1===i&&(i=e.length+1);let n=e.indexOf(s);return-1===n&&(n=e.length+1),i===n?t.localeCompare(s):i-n}}function c(e){if(0===e||"0"===e)return"0s";if(!e)return"--";const t=parseFloat(e);return t?t>60?i.e(t):t.toFixed(2)+"s":e+" seconds"}function d(e,t,s=!0){Object(r.a)(e,t),void 0===e[t]&&e.hasAttribute(t)&&(e[t]=e.getAttribute(t),s&&e.removeAttribute(t))}function h(){return window.innerWidth<600||window.innerHeight<600}function u(e){let t=e.slice(0,-1);if(!/[1-9][0-9]*/.test(t))return null;switch(t=parseInt(t),e.slice(-1)){case"h":t*=60;case"m":t*=60;case"s":break;default:return null}return t}function f(e,t){if(e["human_"+t]="--",e[t]){e[t].endsWith&&!e[t].endsWith("Z")&&(e[t]+="Z"),e[t]=new Date(e[t]);const s=e[t].toString(),i=s.substring(s.indexOf("("));e["human_"+t]=e[t].toLocaleString()+" "+i}}function p(e=[],t=[]){const s=[];for(const t of e)if(t.key&&t.value)if(Array.isArray(t.value))for(const e of t.value)s.push(t.key+":"+e);else s.push(t.key+":"+t.value);else s.push(t);for(let e=2;e<arguments.length;e++)s.push(arguments[e]);const i={f:s,c:t};return"/tasklist?"+n.b(i)}function _(e,t){if(e)return t||(e=e.substring(0,e.length-1)+"0"),`/task?id=${e}`}function m(e){return e?i.c(e.getTime())||"0s":"eons"}function b(e,t){return e?(t||(t=new Date),i.e((t.getTime()-e.getTime())/1e3)||"0s"):"eons"}},function(e,t,s){"use strict";s.d(t,"a",(function(){return i})),s.d(t,"b",(function(){return n}));
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
const i={},n={}},function(e,t,s){"use strict";s.d(t,"c",(function(){return i})),s.d(t,"a",(function(){return n})),s.d(t,"b",(function(){return r}));const i=new Promise((function(e,t){"loading"!==document.readyState?e():document.addEventListener("DOMContentLoaded",e)})),n=(e,t=document)=>Array.prototype.slice.call(t.querySelectorAll(e)),r=(e,t=document)=>t.querySelector(e)},function(e,t,s){"use strict";function i(e,t=1e4){"object"==typeof e&&(e=e.message||JSON.stringify(e));var s={message:e,duration:t};document.dispatchEvent(new CustomEvent("error-sk",{detail:s,bubbles:!0}))}s.d(t,"a",(function(){return i}))},function(e,t,s){"use strict";s.d(t,"a",(function(){return i})),s.d(t,"c",(function(){return n})),s.d(t,"b",(function(){return r}));
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
const i=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,n=(e,t,s=null,i=null)=>{let n=t;for(;n!==s;){const t=n.nextSibling;e.insertBefore(n,i),n=t}},r=(e,t,s=null)=>{let i=t;for(;i!==s;){const t=i.nextSibling;e.removeChild(i),i=t}}},function(e,t,s){"use strict";function i(e){if(e.ok)return e.json();throw{message:`Bad network response: ${e.statusText}`,resp:e,status:e.status}}s.d(t,"a",(function(){return i}))},function(e,t,s){"use strict";function i(e){if(!e)return"";var t=[];return Object.keys(e).sort().forEach((function(s){e[s].forEach((function(e){t.push(encodeURIComponent(s)+"="+encodeURIComponent(e))}))})),t.join("&")}function n(e){var t=[];return Object.keys(e).sort().forEach((function(s){Array.isArray(e[s])?e[s].forEach((function(e){t.push(encodeURIComponent(s)+"="+encodeURIComponent(e))})):"object"==typeof e[s]?t.push(encodeURIComponent(s)+"="+encodeURIComponent(n(e[s]))):t.push(encodeURIComponent(s)+"="+encodeURIComponent(e[s]))})),t.join("&")}function r(e,t){t=t||{};for(var s={},i=e.split("&"),n=0;n<i.length;n++){var o=i[n].split("=",2);if(2==o.length){var a=decodeURIComponent(o[0]),l=decodeURIComponent(o[1]);if(t.hasOwnProperty(a))switch(typeof t[a]){case"boolean":s[a]="true"==l;break;case"number":s[a]=Number(l);break;case"object":if(Array.isArray(t[a])){var c=s[a]||[];c.push(l),s[a]=c}else s[a]=r(l,t[a]);break;case"string":s[a]=l;break;default:s[a]=l}else s[a]=l}}return s}s.d(t,"b",(function(){return i})),s.d(t,"a",(function(){return n})),s.d(t,"c",(function(){return r}))},function(e,t,s){"use strict";s.d(t,"a",(function(){return n})),s.d(t,"b",(function(){return r}));
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
const i=new WeakMap,n=e=>(...t)=>{const s=e(...t);return i.set(s,!0),s},r=e=>"function"==typeof e&&i.has(e)},function(e,t,s){"use strict";s.d(t,"b",(function(){return r})),s.d(t,"a",(function(){return o}));var i=s(8),n=s(2);
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
class r{constructor(e,t,s,i){this.strings=e,this.values=t,this.type=s,this.processor=i}getHTML(){const e=this.strings.length-1;let t="";for(let s=0;s<e;s++){const e=this.strings[s],i=n.e.exec(e);t+=i?e.substr(0,i.index)+i[1]+i[2]+n.b+i[3]+n.f:e+n.g}return t+this.strings[e]}getTemplateElement(){const e=document.createElement("template");return e.innerHTML=this.getHTML(),e}}class o extends r{getHTML(){return`<svg>${super.getHTML()}</svg>`}getTemplateElement(){const e=super.getTemplateElement(),t=e.content,s=t.firstChild;return t.removeChild(s),Object(i.c)(t,s.firstChild),e}}},function(e,t,s){"use strict";s.d(t,"a",(function(){return n})),s.d(t,"e",(function(){return l})),s.d(t,"c",(function(){return c})),s.d(t,"b",(function(){return d})),s.d(t,"d",(function(){return h}));const i=[{units:"w",delta:604800},{units:"d",delta:86400},{units:"h",delta:3600},{units:"m",delta:60},{units:"s",delta:1}],n=1048576,r=1024*n,o=1024*r,a=[{units:" PB",delta:1024*o},{units:" TB",delta:o},{units:" GB",delta:r},{units:" MB",delta:n},{units:" KB",delta:1024},{units:" B",delta:1}];function l(e){if(e<0&&(e=-e),0===e)return"  0s";let t="";for(let s=0;s<i.length;s++)if(i[s].delta<=e){let n=Math.floor(e/i[s].delta)+i[s].units;for(;n.length<4;)n=" "+n;t+=n,e%=i[s].delta}return t}function c(e){let t=(("number"==typeof e?e:Date.parse(e))-Date.now())/1e3;return t<0&&(t*=-1),u(t,i)}function d(e,t=1){return Number.isInteger(t)&&(e*=t),u(e,a)}function h(e){let t=e.toString(),s=t.substring(t.indexOf("("));return e.toLocaleString()+" "+s}function u(e,t){for(let s=0;s<t.length-1;s++){if(Math.round(e/t[s+1].delta)*t[s+1].delta/t[s].delta>=1)return Math.round(e/t[s].delta)+t[s].units}let s=t.length-1;return Math.round(e/t[s].delta)+t[s].units}},function(e,t,s){},,function(e,t,s){"use strict";s.d(t,"a",(function(){return r}));var i=s(8),n=s(2);
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
class r{constructor(e,t,s){this._parts=[],this.template=e,this.processor=t,this.options=s}update(e){let t=0;for(const s of this._parts)void 0!==s&&s.setValue(e[t]),t++;for(const e of this._parts)void 0!==e&&e.commit()}_clone(){const e=i.a?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),t=this.template.parts;let s=0,r=0;const o=e=>{const i=document.createTreeWalker(e,133,null,!1);let a=i.nextNode();for(;s<t.length&&null!==a;){const e=t[s];if(Object(n.d)(e))if(r===e.index){if("node"===e.type){const e=this.processor.handleTextExpression(this.options);e.insertAfterNode(a.previousSibling),this._parts.push(e)}else this._parts.push(...this.processor.handleAttributeExpressions(a,e.name,e.strings,this.options));s++}else r++,"TEMPLATE"===a.nodeName&&o(a.content),a=i.nextNode();else this._parts.push(void 0),s++}};return o(e),i.a&&(document.adoptNode(e),customElements.upgrade(e)),e}}},function(e,t,s){"use strict";s.d(t,"a",(function(){return n}));var i=s(0);
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
 */const n=Object(i.b)(e=>t=>{if(void 0===e&&t instanceof i.a){if(e!==t.value){const e=t.committer.name;t.committer.element.removeAttribute(e)}}else t.setValue(e)})},function(e,t,s){"use strict";function i(e,t){if(!n[t]||"none"===e||!e)return e;let s=n[t][e];if("gpu"===t){const i=e.split("-")[0];s=n[t][i]}else if("os"===t){const i=e.split(".")[0];s=n[t][i]}return s?`${s} (${e})`:e}s.d(t,"a",(function(){return i})),s.d(t,"b",(function(){return o})),s.d(t,"c",(function(){return a}));const n={device:{"iPad4,1":"iPad Air","iPad5,1":"iPad mini 4","iPad6,3":"iPad Pro [9.7 in]","iPhone7,2":"iPhone 6","iPhone9,1":"iPhone 7"},device_type:{angler:"Nexus 6p",athene:"Moto G4",blueline:"Pixel 3",bullhead:"Nexus 5X",crosshatch:"Pixel 3 XL",darcy:"NVIDIA Shield [2017]",dragon:"Pixel C",flame:"Pixel 4",flo:"Nexus 7 [2013]",flounder:"Nexus 9",foster:"NVIDIA Shield [2015]",fugu:"Nexus Player",gce_x86:"Android on GCE",goyawifi:"Galaxy Tab 3",grouper:"Nexus 7 [2012]",hammerhead:"Nexus 5",herolte:"Galaxy S7 [Global]",heroqlteatt:"Galaxy S7 [AT&T]","iPad4,1":"iPad Air","iPad5,1":"iPad mini 4","iPad6,3":"iPad Pro [9.7 in]","iPhone7,2":"iPhone 6","iPhone9,1":"iPhone 7","iPhone10,1":"iPhone 8",j5xnlte:"Galaxy J5",m0:"Galaxy S3",mako:"Nexus 4",manta:"Nexus 10",marlin:"Pixel XL",sailfish:"Pixel",sargo:"Pixel 3a",shamu:"Nexus 6",sprout:"Android One",starlte:"Galaxy S9",taimen:"Pixel 2 XL","TECNO-KB8":"TECNO Spark 3 Pro",walleye:"Pixel 2",zerofltetmo:"Galaxy S6"},gpu:{1002:"AMD","1002:6613":"AMD Radeon R7 240","1002:6646":"AMD Radeon R9 M280X","1002:6779":"AMD Radeon HD 6450/7450/8450","1002:679e":"AMD Radeon HD 7800","1002:6821":"AMD Radeon HD 8870M","1002:683d":"AMD Radeon HD 7770/8760","1002:9830":"AMD Radeon HD 8400","1002:9874":"AMD Carrizo","1a03":"ASPEED","1a03:2000":"ASPEED Graphics Family","102b":"Matrox","102b:0522":"Matrox MGA G200e","102b:0532":"Matrox MGA G200eW","102b:0534":"Matrox G200eR2","10de":"NVIDIA","10de:08a4":"NVIDIA GeForce 320M","10de:08aa":"NVIDIA GeForce 320M","10de:0a65":"NVIDIA GeForce 210","10de:0fe9":"NVIDIA GeForce GT 750M Mac Edition","10de:0ffa":"NVIDIA Quadro K600","10de:104a":"NVIDIA GeForce GT 610","10de:11c0":"NVIDIA GeForce GTX 660","10de:1244":"NVIDIA GeForce GTX 550 Ti","10de:1401":"NVIDIA GeForce GTX 960","10de:1ba1":"NVIDIA GeForce GTX 1070","10de:1cb3":"NVIDIA Quadro P400","10de:2184":"NVIDIA GeForce GTX 1660",8086:"Intel","8086:0046":"Intel Ironlake HD Graphics","8086:0102":"Intel Sandy Bridge HD Graphics 2000","8086:0116":"Intel Sandy Bridge HD Graphics 3000","8086:0166":"Intel Ivy Bridge HD Graphics 4000","8086:0412":"Intel Haswell HD Graphics 4600","8086:041a":"Intel Haswell HD Graphics","8086:0a16":"Intel Haswell HD Graphics 4400","8086:0a26":"Intel Haswell HD Graphics 5000","8086:0a2e":"Intel Haswell Iris Graphics 5100","8086:0d26":"Intel Haswell Iris Pro Graphics 5200","8086:0f31":"Intel Bay Trail HD Graphics","8086:1616":"Intel Broadwell HD Graphics 5500","8086:161e":"Intel Broadwell HD Graphics 5300","8086:1626":"Intel Broadwell HD Graphics 6000","8086:162b":"Intel Broadwell Iris Graphics 6100","8086:1912":"Intel Skylake HD Graphics 530","8086:191e":"Intel Skylake HD Graphics 515","8086:1926":"Intel Skylake Iris 540/550","8086:193b":"Intel Skylake Iris Pro 580","8086:22b1":"Intel Braswell HD Graphics","8086:3e92":"Intel Coffee Lake UHD Graphics 630","8086:3ea5":"Intel Coffee Lake Iris Plus Graphics 655","8086:5912":"Intel Kaby Lake HD Graphics 630","8086:591e":"Intel Kaby Lake HD Graphics 615","8086:5926":"Intel Kaby Lake Iris Plus Graphics 640"},os:{"Windows-10-10240":"Windows 10 version 1507","Windows-10-10586":"Windows 10 version 1511","Windows-10-14393":"Windows 10 version 1607","Windows-10-15063":"Windows 10 version 1703","Windows-10-16299":"Windows 10 version 1709","Windows-10-17134":"Windows 10 version 1803","Windows-10-17763":"Windows 10 version 1809","Windows-10-18362":"Windows 10 version 1903","Windows-10-18363":"Windows 10 version 1909","Windows-Server-14393":"Windows Server 2016","Windows-Server-17134":"Windows Server version 1803","Windows-Server-17763":"Windows Server 2019 or version 1809","Windows-Server-18362":"Windows Server version 1903","Windows-Server-18363":"Windows Server version 1909"}},r=/.+\((.+)\)/;function o(e){return e?e.map(e=>{const t=e.split(":")[0];if(n[t]){const s=e.match(r);return s?t+":"+s[1]:e}return e}):[]}function a(e){const t=e.indexOf(":");if(t<0)return e;const s=e.substring(0,t),n=e.substring(t+1),r=s.split("-tag")[0];return`${s}:${i(n,r)}`}},function(e,t){e.exports=function e(t,s){"use strict";var i,n,r=/(^([+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?)?$|^0x[0-9a-f]+$|\d+)/gi,o=/(^[ ]*|[ ]*$)/g,a=/(^([\w ]+,?[\w ]+)?[\w ]+,?[\w ]+\d+:\d+(:\d+)?[\w ]?|^\d{1,4}[\/\-]\d{1,4}[\/\-]\d{1,4}|^\w+, \w+ \d+, \d{4})/,l=/^0x[0-9a-f]+$/i,c=/^0/,d=function(t){return e.insensitive&&(""+t).toLowerCase()||""+t},h=d(t).replace(o,"")||"",u=d(s).replace(o,"")||"",f=h.replace(r,"\0$1\0").replace(/\0$/,"").replace(/^\0/,"").split("\0"),p=u.replace(r,"\0$1\0").replace(/\0$/,"").replace(/^\0/,"").split("\0"),_=parseInt(h.match(l),16)||1!==f.length&&h.match(a)&&Date.parse(h),m=parseInt(u.match(l),16)||_&&u.match(a)&&Date.parse(u)||null;if(m){if(_<m)return-1;if(_>m)return 1}for(var b=0,g=Math.max(f.length,p.length);b<g;b++){if(i=!(f[b]||"").match(c)&&parseFloat(f[b])||f[b]||0,n=!(p[b]||"").match(c)&&parseFloat(p[b])||p[b]||0,isNaN(i)!==isNaN(n))return isNaN(i)?1:-1;if(typeof i!=typeof n&&(i+="",n+=""),i<n)return-1;if(i>n)return 1}return 0}},,function(e,t,s){"use strict";s.d(t,"a",(function(){return o}));var i=s(7),n=s(0),r=s(1);class o extends HTMLElement{constructor(e){super(),this._template=e,this._app=null,this._auth_header="",this._profile=null,this._notAuthorized=!1}connectedCallback(){Object(r.a)(this,"client_id"),Object(r.a)(this,"testing_offline"),this._authHeaderEvent=e=>{this._auth_header=e.detail.auth_header},this.addEventListener("log-in",this._authHeaderEvent)}disconnectedCallback(){this.removeEventListener("log-in",this._authHeaderEvent)}static get observedAttributes(){return["client_id","testing_offline"]}get app(){return this._app}get auth_header(){return this._auth_header}get loggedInAndAuthorized(){return!!this._auth_header&&!this._notAuthorized}get permissions(){return this._app&&this._app.permissions||{}}get profile(){return this._app&&this._app.profile||{}}get server_details(){return this._app&&this._app.server_details||{}}get client_id(){return this.getAttribute("client_id")}set client_id(e){return this.setAttribute("client_id",e)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(e){e?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}fetchError(e,t){403===e.status?(this._message="User unauthorized - try logging in with a different account",this._notAuthorized=!0,this.render()):"AbortError"!==e.name&&(console.error(e),Object(i.a)(`Unexpected error loading ${t}: ${e.message}`,5e3)),this._app.finishedTask()}render(){Object(n.d)(this._template(this),this,{eventContext:this}),this._app||(this._app=this.firstElementChild,Object(n.d)(this._template(this),this,{eventContext:this}))}attributeChangedCallback(e,t,s){this.render()}}},function(e,t,s){"use strict";s.d(t,"a",(function(){return n})),s.d(t,"b",(function(){return r})),s.d(t,"c",(function(){return o})),s.d(t,"d",(function(){return a}));var i=s(18);function n(e,t){return t?e.filter(e=>l(e,t)):e}function r(e,t,s){if(!s)return e;if(-1===(s=s.trim()).indexOf(":"))return e.filter(e=>{if(l(e,s))return!0;let n=t[e]||[];for(let t of n)if(t=Object(i.a)(t,e),l(t,s))return!0;return!1});const n=(s=s.split(":")[0])+"-tag";return e.filter(e=>e===s||e===n)}function o(e,t,s){const n=(s=s.trim()).indexOf(":");return-1!==n&&(s=s.substring(n+1)),!s||l(t,s)?e:e.filter(e=>!!l(e=Object(i.a)(e,t),s))}function a(e,t){return`${e}:${t}`}function l(e,t){if(!t)return!0;if(!e)return!1;t=t.trim().toLocaleLowerCase(),e=e.toLocaleLowerCase();const s=t.split(" ");for(const t of s){if(-1!==e.indexOf(t))return!0}return!1}},function(e,t,s){"use strict";s.d(t,"a",(function(){return a}));var i=s(10);const n=e=>JSON.parse(JSON.stringify(e));function r(e,t){let s={};return Object.keys(e).forEach((function(n){(function(e,t){if(typeof e!=typeof t)return!1;let s=typeof e;return"string"===s||"boolean"===s||"number"===s?e===t:"object"===s?Array.isArray(s)?JSON.stringify(e)===JSON.stringify(t):Object(i.a)(e)===Object(i.a)(t):void 0})(e[n],t[n])||(s[n]=e[n])})),s}var o=s(6);function a(e,t){let s=n(e()),a=!1;const l=()=>{a=!0;let e=i.c(window.location.search.slice(1),s);t(function(e,t){let s={};return Object.keys(t).forEach((function(i){e.hasOwnProperty(i)?s[i]=n(e[i]):s[i]=n(t[i])})),s}(e,s))};return o.c.then(l),window.addEventListener("popstate",l),()=>{if(!a)return;let t=i.a(r(e(),s));history.pushState(null,"",window.location.origin+window.location.pathname+"?"+t)}}},function(e,t,s){"use strict";s(32)},function(e,t,s){},function(e,t,s){},function(e,t,s){},function(e,t,s){},function(e,t,s){"use strict";var i=s(7),n=s(0),r=s(17),o=s(9),a=s(1);window.customElements.define("toast-sk",class extends HTMLElement{constructor(){super(),this._timer=null}connectedCallback(){this.hasAttribute("duration")||(this.duration=5e3),Object(a.a)(this,"duration")}get duration(){return+this.getAttribute("duration")}set duration(e){this.setAttribute("duration",e)}show(){this.setAttribute("shown",""),this.duration>0&&!this._timer&&(this._timer=window.setTimeout(()=>{this._timer=null,this.hide()},this.duration))}hide(){this.removeAttribute("shown"),this._timer&&(window.clearTimeout(this._timer),this._timer=null)}});s(25);window.customElements.define("error-toast-sk",class extends HTMLElement{connectedCallback(){this.innerHTML="<toast-sk></toast-sk>",this._toast=this.firstElementChild,document.addEventListener("error-sk",this)}disconnectedCallback(){document.removeEventListener("error-sk",this)}handleEvent(e){e.detail.duration&&(this._toast.duration=e.detail.duration),this._toast.textContent=e.detail.message,this._toast.show()}});s(14);const l=document.createElement("template");l.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M20 8h-2.81c-.45-.78-1.07-1.45-1.82-1.96L17 4.41 15.59 3l-2.17 2.17C12.96 5.06 12.49 5 12 5c-.49 0-.96.06-1.41.17L8.41 3 7 4.41l1.62 1.63C7.88 6.55 7.26 7.22 6.81 8H4v2h2.09c-.05.33-.09.66-.09 1v1H4v2h2v1c0 .34.04.67.09 1H4v2h2.81c1.04 1.79 2.97 3 5.19 3s4.15-1.21 5.19-3H20v-2h-2.09c.05-.33.09-.66.09-1v-1h2v-2h-2v-1c0-.34-.04-.67-.09-1H20V8zm-6 8h-4v-2h4v2zm0-4h-4v-2h4v2z"/></svg>',window.customElements.define("bug-report-icon-sk",class extends HTMLElement{connectedCallback(){let e=l.content.cloneNode(!0);this.appendChild(e)}});const c=document.createElement("template");c.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>',window.customElements.define("menu-icon-sk",class extends HTMLElement{connectedCallback(){let e=c.content.cloneNode(!0);this.appendChild(e)}}),window.customElements.define("spinner-sk",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"active")}get active(){return this.hasAttribute("active")}set active(e){e?this.setAttribute("active",""):this.removeAttribute("active")}});s(26),s(27);const d=new Promise((e,t)=>{const s=()=>{void 0!==window.gapi?e():setTimeout(s,10)};setTimeout(s,10)});window.customElements.define("oauth-login",class extends HTMLElement{connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._auth_header="",this.testing_offline?this._profile={email:"missing@chromium.org",imageURL:"http://storage.googleapis.com/gd-wagtail-prod-assets/original_images/logo_google_fonts_color_2x_web_64dp.png"}:(this._profile=null,d.then(()=>{gapi.load("auth2",()=>{gapi.auth2.init({client_id:this.client_id}).then(()=>{this._maybeFireLoginEvent(),this.render()},e=>{console.error(e),Object(i.a)(`Error initializing oauth: ${JSON.stringify(e)}`,1e4)})})})),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get auth_header(){return this._auth_header}get client_id(){return this.getAttribute("client_id")}set client_id(e){return this.setAttribute("client_id",e)}get profile(){return this._profile}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(e){e?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}_maybeFireLoginEvent(){const e=gapi.auth2.getAuthInstance().currentUser.get();if(e.isSignedIn()){const t=e.getBasicProfile();this._profile={email:t.getEmail(),imageURL:t.getImageUrl()};const s=e.getAuthResponse(!0),i=`${s.token_type} ${s.access_token}`;return this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:i,profile:this._profile},bubbles:!0})),this._auth_header=i,!0}return this._profile=null,this._auth_header="",!1}_logIn(){if(this.testing_offline)this._auth_header="Bearer 12345678910-boomshakalaka",this.dispatchEvent(new CustomEvent("log-in",{detail:{auth_header:this._auth_header,profile:this._profile},bubbles:!0})),this.render();else{const e=gapi.auth2.getAuthInstance();e&&e.signIn({scope:"email",prompt:"select_account"}).then(()=>{this._maybeFireLoginEvent()||console.warn("login was not successful; maybe user canceled"),this.render()})}}_logOut(){if(this.testing_offline)this._auth_header="",this.render(),window.location.reload();else{const e=gapi.auth2.getAuthInstance();e&&e.signOut().then(()=>{this._auth_header="",this._profile=null,window.location.reload()})}}render(){var e;Object(n.d)((e=this).auth_header?n.c`
<div>
  <img class=center id=avatar src="${e._profile.imageURL}" width=30 height=30>
  <span class=center>${e._profile.email}</span>
  <span class=center>|</span>
  <a class=center @click=${e._logOut} href="#">Sign out</a>
</div>`:n.c`
<div>
  <a @click=${e._logIn} href="#">Sign in</a>
</div>`,this,{eventContext:this})}attributeChangedCallback(e,t,s){this.render()}});const h=document.createElement("template");h.innerHTML="\n<button class=toggle-button>\n  <menu-icon-sk>\n  </menu-icon-sk>\n</button>\n";const u=document.createElement("template");u.innerHTML="\n<div class=spinner-spacer>\n  <spinner-sk></spinner-sk>\n</div>\n";const f=document.createElement("template");f.innerHTML='\n<a target=_blank rel=noopener\n   href="https://bugs.chromium.org/p/chromium/issues/entry?components=Infra%3EPlatform%3ESwarming%3EWebUI&owner=kjlubick@chromium.org&status=Assigned">\n  <bug-report-icon-sk class=fab></bug-report-icon-sk>\n</a>',window.customElements.define("swarming-app",class extends HTMLElement{constructor(){super(),this._busyTaskCount=0,this._spinner=null,this._dynamicEle=null,this._auth_header="",this._profile={},this._server_details={server_version:"You must log in to see more details",bot_version:""},this._permissions={}}connectedCallback(){Object(a.a)(this,"client_id"),Object(a.a)(this,"testing_offline"),this._addHTML(),this.addEventListener("log-in",e=>{this._auth_header=e.detail.auth_header,this._profile=e.detail.profile,this._fetch()}),this.render()}static get observedAttributes(){return["client_id","testing_offline"]}get busy(){return!!this._busyTaskCount}get permissions(){return this._permissions}get profile(){return this._profile}get server_details(){return this._server_details}get client_id(){return this.getAttribute("client_id")}set client_id(e){return this.setAttribute("client_id",e)}get testing_offline(){return this.hasAttribute("testing_offline")}set testing_offline(e){e?this.setAttribute("testing_offline",!0):this.removeAttribute("testing_offline")}addBusyTasks(e){this._busyTaskCount+=e,this._spinner&&this._busyTaskCount>0&&(this._spinner.active=!0)}finishedTask(){this._busyTaskCount--,this._busyTaskCount<=0&&(this._busyTaskCount=0,this._spinner&&(this._spinner.active=!1),this.dispatchEvent(new CustomEvent("busy-end",{bubbles:!0})))}_addHTML(){const e=this.querySelector("header"),t=e&&e.querySelector("aside"),s=this.querySelector("footer");if(!(e&&t&&t.classList.contains("hideable")))return;let i=h.content.cloneNode(!0);e.insertBefore(i,e.firstElementChild),i=e.firstElementChild,i.addEventListener("click",e=>this._toggleMenu(e,t));const n=u.content.cloneNode(!0);e.insertBefore(n,t),this._spinner=e.querySelector("spinner-sk");const r=document.createElement("span");r.classList.add("grow"),e.appendChild(r),this._dynamicEle=document.createElement("div"),this._dynamicEle.classList.add("right"),e.appendChild(this._dynamicEle);const o=document.createElement("error-toast-sk");s.append(o);const a=f.content.cloneNode(!0);s.append(a)}_toggleMenu(e,t){t.classList.toggle("shown")}_fetch(){if(!this._auth_header)return;this._server_details={server_version:"<loading>",bot_version:"<loading>"};const e={headers:{authorization:this._auth_header}};this.addBusyTasks(1),fetch("/_ah/api/swarming/v1/server/details",e).then(o.a).then(e=>{this._server_details=e,this.render(),this.dispatchEvent(new CustomEvent("server-details-loaded",{bubbles:!0})),this.finishedTask()}).catch(e=>{403===e.status?(this._server_details={server_version:"User unauthorized - try logging in with a different account",bot_version:""},this.render()):(console.error(e),Object(i.a)(`Unexpected error loading details: ${e.message}`,5e3)),this.finishedTask()}),this._fetchPermissions(e)}_fetchPermissions(e,t){this.addBusyTasks(1);let s="/_ah/api/swarming/v1/server/permissions";if(t){const e=new URLSearchParams;for(const[s,i]of Object.entries(t))e.append(s,i);s+=`?${e.toString()}`}fetch(s,e).then(o.a).then(e=>{this._permissions=e,this.render(),this.dispatchEvent(new CustomEvent("permissions-loaded",{bubbles:!0})),this.finishedTask()}).catch(e=>{403!==e.status&&(console.error(e),Object(i.a)(`Unexpected error loading permissions: ${e.message}`,5e3)),this.finishedTask()})}render(){var e;this._dynamicEle&&Object(n.d)((e=this,n.c`
<div class=server-version>
  Server:
  <a href=${Object(r.a)(function(e){if(e&&e.server_version){var t=e.server_version.split("-");if(2===t.length)return`https://chromium.googlesource.com/infra/luci/luci-py/+/${t[1]}`}}(e._server_details))}>
    ${e._server_details.server_version}
  </a>
</div>
<oauth-login client_id=${e.client_id}
             ?testing_offline=${e.testing_offline}>
</oauth-login>`),this._dynamicEle)}attributeChangedCallback(e,t,s){this.render()}});s(28)},function(e,t,s){"use strict";var i=s(1);class n extends HTMLElement{get _role(){return"checkbox"}static get observedAttributes(){return["checked","disabled","name","label"]}connectedCallback(){this.innerHTML=`<label><input type=${this._role}></input><span class=box></span><span class=label></span></label>`,this._label=this.querySelector(".label"),this._input=this.querySelector("input"),Object(i.a)(this,"checked"),Object(i.a)(this,"disabled"),Object(i.a)(this,"name"),Object(i.a)(this,"label"),this._input.checked=this.checked,this._input.disabled=this.disabled,this._input.setAttribute("name",this.getAttribute("name")),this._label.textContent=this.getAttribute("label")}get checked(){return this.hasAttribute("checked")}set checked(e){let t=!!e;this._input.checked=t,e?this.setAttribute("checked",""):this.removeAttribute("checked")}get disabled(){return this.hasAttribute("disabled")}set disabled(e){let t=!!e;this._input.disabled=t,t?this.setAttribute("disabled",""):this.removeAttribute("disabled")}get name(){return this._input.getAttribute("name")}set name(e){this.setAttribute("name",e),this._input.setAttribute("name",e)}get label(){return this._input.getAttribute("label")}set label(e){this.setAttribute("label",e),this._input.setAttribute("label",e)}attributeChangedCallback(e,t,s){if(!this._input)return;let i=null!=s;switch(e){case"checked":this._input.checked=i;break;case"disabled":this._input.disabled=i;break;case"name":this._input.name=s;break;case"label":this._label.textContent=s}}}window.customElements.define("checkbox-sk",n);s(31)},function(e,t,s){},function(e,t,s){},function(e,t,s){},function(e,t,s){"use strict";var i=s(6);const n=document.createElement("template");n.innerHTML="<div class=backdrop></div>",window.customElements.define("dialog-pop-over",class extends HTMLElement{constructor(){super(),this._backdrop=null,this._content=null}connectedCallback(){const e=n.content.cloneNode(!0);if(this.appendChild(e),this._backdrop=Object(i.b)(".backdrop",this),this._content=Object(i.b)(".content",this),!this._content)throw"You must have an element with class content to show."}hide(){this._backdrop.classList.remove("opened"),this._content.classList.remove("opened")}show(){const e=window.innerWidth,t=window.innerHeight,s=Math.min(this._content.offsetWidth,e-50),i=Math.min(this._content.offsetHeight,t-50);this._content.style.width=s,this._content.style.left=(e-s)/2,this._content.style.top=(t-i)/2,this._backdrop.classList.add("opened"),this._content.classList.add("opened")}});s(33)},function(e,t,s){"use strict";s.d(t,"a",(function(){return o}));var i=s(3),n=s(0);
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
const r=new WeakMap,o=Object(n.b)((...e)=>t=>{let s=r.get(t);void 0===s&&(s={values:[]},r.set(t,s));const n=s.values;s.values=e;for(let r=0;r<e.length&&!(void 0!==s.lastRenderedIndex&&r>s.lastRenderedIndex);r++){const o=e[r];if(Object(i.g)(o)||"function"!=typeof o.then){t.setValue(o),s.lastRenderedIndex=r;break}void 0!==s.lastRenderedIndex&&"function"==typeof o.then&&o===n[r]||(s.lastRenderedIndex=void 0,Promise.resolve(o).then(e=>{const i=s.values.indexOf(o);i>-1&&(void 0===s.lastRenderedIndex||i<s.lastRenderedIndex)&&(s.lastRenderedIndex=i,t.setValue(e),t.commit())}))}})},function(e,t,s){"use strict";s.d(t,"a",(function(){return o}));var i=s(0);s(14);const n=document.createElement("template");n.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"/></svg>',window.customElements.define("expand-less-icon-sk",class extends HTMLElement{connectedCallback(){let e=n.content.cloneNode(!0);this.appendChild(e)}});const r=document.createElement("template");function o(e){return e?i.c`<expand-less-icon-sk></expand-less-icon-sk>`:i.c`<expand-more-icon-sk></expand-more-icon-sk>`}r.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>',window.customElements.define("expand-more-icon-sk",class extends HTMLElement{connectedCallback(){let e=r.content.cloneNode(!0);this.appendChild(e)}})},function(e,t,s){},function(e,t,s){"use strict";var i=s(0),n=s(4);s(14);const r=document.createElement("template");r.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>',window.customElements.define("arrow-drop-down-icon-sk",class extends HTMLElement{connectedCallback(){let e=r.content.cloneNode(!0);this.appendChild(e)}});const o=document.createElement("template");o.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M7 14l5-5 5 5z"/></svg>',window.customElements.define("arrow-drop-up-icon-sk",class extends HTMLElement{connectedCallback(){let e=o.content.cloneNode(!0);this.appendChild(e)}});window.customElements.define("sort-toggle",class extends HTMLElement{constructor(){super()}connectedCallback(){Object(n.e)(this,"currentKey"),Object(n.e)(this,"key"),Object(n.e)(this,"direction"),this.addEventListener("click",()=>{this.toggle()}),this.render()}get currentKey(){return this._currentKey}set currentKey(e){this._currentKey=e,this.render()}get key(){return this._key}set key(e){this._key=e,this.render()}get direction(){return this._direction}set direction(e){this._direction=e,this.render()}toggle(){this.currentKey===this.key&&"asc"===this.direction?this.direction="desc":this.direction="asc",this.dispatchEvent(new CustomEvent("sort-change",{detail:{direction:this.direction,key:this.key},bubbles:!0}))}render(){var e;Object(i.d)((e=this,i.c`
<arrow-drop-down-icon-sk ?hidden=${e.key===e.currentKey&&"asc"===e.direction}>
</arrow-drop-down-icon-sk>
<arrow-drop-up-icon-sk ?hidden=${e.key===e.currentKey&&"desc"===e.direction}>
</arrow-drop-up-icon-sk>`),this,{eventContext:this})}});s(37)},,,function(e,t,s){"use strict";s(14);const i=document.createElement("template");i.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>',window.customElements.define("add-circle-icon-sk",class extends HTMLElement{connectedCallback(){let e=i.content.cloneNode(!0);this.appendChild(e)}})},function(e,t,s){"use strict";s(14);const i=document.createElement("template");i.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg>',window.customElements.define("cancel-icon-sk",class extends HTMLElement{connectedCallback(){let e=i.content.cloneNode(!0);this.appendChild(e)}})},function(e,t,s){"use strict";s(14);const i=document.createElement("template");i.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>',window.customElements.define("more-vert-icon-sk",class extends HTMLElement{connectedCallback(){let e=i.content.cloneNode(!0);this.appendChild(e)}})},function(e,t,s){"use strict";s(14);const i=document.createElement("template");i.innerHTML='<svg class="icon-sk-svg" xmlns="http://www.w3.org/2000/svg" width=24 height=24 viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>',window.customElements.define("search-icon-sk",class extends HTMLElement{connectedCallback(){let e=i.content.cloneNode(!0);this.appendChild(e)}})},function(e,t,s){},function(e,t,s){"use strict";var i=s(1);window.customElements.define("select-sk",class extends HTMLElement{constructor(){super(),this._obs=new MutationObserver(()=>this._bubbleUp()),this._selection=-1}connectedCallback(){Object(i.a)(this,"selection"),Object(i.a)(this,"disabled"),this.addEventListener("click",this._click),this._obs.observe(this,{childList:!0}),this._bubbleUp()}disconnectedCallback(){this.removeEventListener("click",this._click),this._obs.disconnect()}get disabled(){return this.hasAttribute("disabled")}set disabled(e){e?(this.setAttribute("disabled",""),this.selection=-1):(this.removeAttribute("disabled"),this._bubbleUp())}get selection(){return this._selection}set selection(e){this.disabled||(null==e&&(e=-1),this._selection=+e,this._rationalize())}_click(e){if(this.disabled)return;let t=this._selection,s=e.target;for(;s&&s.parentElement!==this;)s=s.parentElement;if(s&&s.parentElement===this)for(let e=0;e<this.children.length;e++)if(this.children[e]===s){this._selection=e;break}this._rationalize(),t!=this._selection&&this.dispatchEvent(new CustomEvent("selection-changed",{detail:{selection:this._selection},bubbles:!0}))}_rationalize(){for(let e=0;e<this.children.length;e++)this._selection===e?this.children[e].setAttribute("selected",""):this.children[e].removeAttribute("selected")}_bubbleUp(){if(this._selection=-1,!this.disabled){for(let e=0;e<this.children.length;e++)if(this.children[e].hasAttribute("selected")){this._selection=e;break}this._rationalize()}}});s(45)},,,,function(e,t,s){},function(e,t,s){},,,,,,,,,function(e,t,s){"use strict";s.r(t);var i=s(6),n=s(7),r=s(0),o=s(17),a=s(9),l=s(19),c=s.n(l),d=s(10),h=s(23),u=(s(30),s(41),s(42),s(43),s(44),s(46),s(24),s(35)),f=s(4);const p=e=>r.c`<li>${e}</li>`;function _(e,t){const s=`Unexpected error loading ${t}: ${e.message}`;console.error(s),Object(n.a)(s,5e3)}window.customElements.define("bot-mass-delete",class extends HTMLElement{constructor(){super(),this._count="...",this._readyToDelete=!1,this._started=!1,this._finished=!1,this._progress=0}connectedCallback(){Object(f.e)(this,"auth_header"),Object(f.e)(this,"dimensions"),"string"==typeof this.dimensions&&(this.dimensions=this.dimensions.split(",")),this.dimensions.sort(),this.render()}_deleteAll(){this._started=!0,this.dispatchEvent(new CustomEvent("bots-deleting-started",{bubbles:!0}));const e=d.a({dimensions:this.dimensions,limit:200,fields:"cursor,items/bot_id",is_dead:"TRUE"}),t={headers:{authorization:this.auth_header}};let s=[];fetch(`/_ah/api/swarming/v1/bots/list?${e}`,t).then(a.a).then(e=>{const i=e=>{if(s=s.concat(e.items),this.render(),e.cursor){const s=d.a({cursor:e.cursor,dimensions:this.dimensions,limit:200,fields:"cursor,items/bot_id",is_dead:"TRUE"});fetch(`/_ah/api/swarming/v1/bots/list?${s}`,t).then(a.a).then(i).catch(e=>_(e,"bot-mass-delete/list (paging)"))}else{const e={headers:{authorization:this.auth_header},method:"POST"},t=s=>{if(!s.length)return this._finished=!0,this.render(),void this.dispatchEvent(new CustomEvent("bots-deleting-finished",{bubbles:!0}));const i=s.pop();fetch(`/_ah/api/swarming/v1/bot/${i.bot_id}/delete`,e).then(()=>{this._progress++,this.render(),t(s)}).catch(e=>_(e,"bot-mass-delete/delete"))};t(s)}};i(e)}).catch(e=>_(e,"bot-mass-delete/list")),this.render()}_fetchCount(){if(!this.auth_header)return void console.warn("no auth_header recieved, try refreshing the page?");const e={headers:{authorization:this.auth_header}},t=d.a({dimensions:this.dimensions}),s=fetch(`/_ah/api/swarming/v1/bots/count?${t}`,e).then(a.a).then(e=>(this._readyToDelete=!0,this.render(),parseInt(e.dead))).catch(e=>_(e,"bot-mass-delete/count"));this._count=r.c`${Object(u.a)(s,"...")}`}render(){var e;Object(r.d)((e=this,r.c`
  <div>
    You are about to delete all DEAD bots with the following dimensions:
    <ul>
      ${e.dimensions.map(p)}
    </ul>

    This is about ${e._count} bots.
    Once you start the process, the only way to partially stop it is to close this
    browser window.

    If that sounds good, click the button below.
  </div>

  <button class=delete ?disabled=${!e._readyToDelete||e._started}
                       @click=${e._deleteAll}
                       tabindex=0>
    Delete the bots
  </button>

  <div>
    <div ?hidden=${!e._started}>
      Progress: ${e._progress} deleted${e._finished?" - DONE.":"."}
    </div>
    <div>
      Note: the bot deletion is being done in browser -
      closing the window will stop the mass deletion.
    </div>
  </div>
`),this,{eventContext:this})}show(){this._readyToDelete=!1,this._started=!1,this._finished=!1,this._progress=0,this._fetchCount(),this.render()}});s(50),s(34),s(38),s(29);var m=s(18),b=s(13);function g(e){if(!e)return{};const t=[];let s=0;for(const i in e)t.push(i+": "+e[i]),s+=+e[i];return s/=t.length,s=s?s.toFixed(1):"unknown",{average:s,zones:t.join(" | ")||"unknown"}}function v(e,t,s){return s=s||"UNKNOWN",k(e,t)||x(e,t)||[s]}function y(e,t,s){if(!t)return console.warn("falsey bot passed into column"),"";const i=B[e];if(i)return i(t,s);let n="--";return-1!==$.indexOf(e)&&(n="none"),function(e,t){if(t)return e.join(" | ");let s="";for(let t=0;t<e.length;t++)e[t]&&e[t].length>s.length&&(s=e[t]);return s}(v(t,e,n).map(t=>Object(m.a)(t,e)),s._verbose)}const w={id:function(e,t){return e.bot_id===t},status:function(e,t){return"quarantined"===t?e.quarantined:"maintenance"===t?!!e.maintenance_msg:"dead"===t?e.is_dead:!e.is_dead},task:function(e,t){return"idle"===t?!e.task_id:!!e.task_id}};function k(e,t){if(!e||!e.dimensions||!t)return null;for(let s=0;s<e.dimensions.length;s++)if(e.dimensions[s].key===t)return e.dimensions[s].value;return null}function x(e,t){if(!e||!e.state||!e.state[t])return null;const s=e.state[t];return Array.isArray(s)?s:[s]}const C=["All","Alive","Busy","Idle","Dead","Quarantined","Maintenance"];function E(){return C.map(e=>({label:e,key:""}))}function A(e,t,s){const i={},n=[];for(const t of e){const e=t.split(":",1)[0],s=t.substring(e.length+1);"status"===e?"alive"===s?i.is_dead=["FALSE"]:"quarantined"===s?i.quarantined=["TRUE"]:"maintenance"===s?i.in_maintenance=["TRUE"]:"dead"===s&&(i.is_dead=["TRUE"]):"task"===e?"busy"===s?i.is_busy=["TRUE"]:"idle"===s&&(i.is_busy=["FALSE"]):n.push(e+":"+s)}return i.dimensions=n,i.limit=t,s&&(i.cursor=s),d.a(i)}const O=["first_seen_ts","last_seen_ts","lease_expiration_ts"];function N(e,t){return e[0].value=parseInt(t.count),e[1].value=parseInt(t.count)-parseInt(t.dead),e[2].value=parseInt(t.busy),e[3].value=parseInt(t.count)-parseInt(t.busy),e[4].value=parseInt(t.dead),e[5].value=parseInt(t.quarantined),e[6].value=parseInt(t.maintenance),e}const $=["device_os","device_type","gpu"];const T=Object(f.c)(["id","task"]);const I={cores:!0,cpu:!0,gpu:!0,"host-cpu":!0,machine_type:!0,os:!0,python:!0,xcode_version:!0,zone:!0};const L=["quarantined","error","id"],S=["disk_space","uptime","running_time","task","status","version","external_ip","internal_ip","last_seen","first_seen","battery_level","battery_voltage","battery_temperature","battery_status","battery_health","bot_temperature","device_temperature","serial_number"],j={id:"Bot Id",task:"Current Task",android_devices:"Android Devices",battery_health:"Battery Health",battery_level:"Battery Level (%)",battery_status:"Battery Status",battery_temperature:"Battery Temp (°C)",battery_voltage:"Battery Voltage (mV)",bot_temperature:"Bot Temp (°C)",cores:"CPU Core Count",cpu:"CPU type",device:"Non-android Device",device_os:"Device OS",device_temperature:"Device Temp (°C)",device_type:"Device Type",disk_space:"Free Space (MB)",external_ip:"External IP",first_seen:"First Seen",gpu:"GPU type",internal_ip:"Internal or Local IP",last_seen:"Last Seen",os:"OS",pool:"Pool",running_time:"Swarming Uptime",serial_number:"Device Serial Number",status:"Status",uptime:"Bot Uptime",xcode_version:"XCode Version",version:"Client Code Version"},M={1:"Unknown",2:"Good",3:"Overheated",4:"Dead",5:"Over Voltage",6:"Unspecified Failure",7:"Too Cold"},P={1:"Unknown",2:"Charging",3:"Discharging",4:"Not Charging",5:"Full"};function D(e){return e.is_dead?4:e.quarantined?3:e.maintenance_msg?2:1}const H=["id"],V={disk_space:(e,t,s)=>e*c()(t.disks[0].mb,s.disks[0].mb),id:(e,t,s)=>e*c()(t.bot_id,s.bot_id),first_seen:(e,t,s)=>e*c()(t.first_seen_ts,s.first_seen_ts),last_seen:(e,t,s)=>e*c()(t.last_seen_ts,s.last_seen_ts),status:(e,t,s)=>{const i=D(t),n=D(s);return i!==n?e*(i-n):t.is_dead||t.quarantined||t.maintenance_msg?e*(t.last_seen_ts-s.last_seen_ts):0},running_time:(e,t,s)=>e*c()(x(t,"running_time"),x(s,"running_time")),uptime:(e,t,s)=>e*c()(x(t,"uptime"),x(s,"uptime"))};function U(e){return(t,s)=>{const i=t.state.devices;return i&&i.length?i.map(e).join(" | "):"N/A - no devices"}}const B={android_devices:(e,t)=>{const s=v(e,"android_devices","0");return t._verbose?s.join(" | ")+" devices available":Math.max(...s)+" devices available"},battery_health:U(e=>{const t=e.battery&&e.battery.health||"UNKNOWN";return`${M[t]||""} (${t})`}),battery_level:U(e=>e.battery&&e.battery.level||"UNKNOWN"),battery_status:U(e=>{const t=e.battery&&e.battery.status||"UNKNOWN";return`${P[t]||""} (${t})`}),battery_temperature:U(e=>e.battery&&e.battery.temperature/10||"UNKNOWN"),battery_voltage:U(e=>e.battery&&e.battery.voltage||"UNKNOWN"),bot_temperature:(e,t)=>t._verbose?e.state.temp.zones||"UNKNOWN":e.state.temp.average||"UNKNOWN",device_temperature:(e,t)=>{const s=e.state.devices;return s&&s.length?s.map(e=>t._verbose?e.temp.zones||UNKNOWN:e.temp.average||UNKNOWN).join(" | "):"N/A - no devices"},disk_space:(e,t)=>{const s=[];for(const t of e.disks){const e=b.b(t.mb,b.a);s.push(`${t.id} ${e} (${t.mb})`)}return t._verbose?s.join(" | "):s[0]},external_ip:(e,t)=>e.external_ip||"--",first_seen:(e,t)=>b.d(e.first_seen_ts),id:(e,t)=>{return r.c`<a target=_blank
                            rel=noopener
                            href=${s=e.bot_id,`/bot?id=${s}`}>${e.bot_id}</a>`;var s},internal_ip:(e,t)=>v(e,"ip","--")[0],last_seen:(e,t)=>{return t._verbose?b.d(e.last_seen_ts):((s=e.last_seen_ts)?b.c(s.getTime()):"eons")+" ago";var s},running_time:(e,t)=>{const s=x(e,"running_time");return s?b.e(s):"UNKNOWN"},serial_number:U(e=>e.serial||"UNKNOWN"),status:(e,t)=>{if(e.is_dead)return`Dead. Last seen ${b.c(e.last_seen_ts)} ago`;if(e.quarantined){let t=x(e,"quarantined");t&&(t=t[0]),t&&"true"!==t&&!0!==t||(t=v(e,"error")[0]),"UNKNOWN"===t&&(t=k(e,"quarantined")||"UNKNOWN");const s=[];return function(e){return e.state.devices||[]}(e).forEach((function(e){s.push(e.state)})),s.length&&(t+=` devices: [${s.join(", ")}]`),`Quarantined: ${t}`}return e.maintenance_msg?`Maintenance: ${e.maintenance_msg}`:"Alive"},task:(e,t)=>{if(!e.task_id)return"idle";let s=e.task_id,i=e.task_name;return e.is_dead&&(s="[died on task]",i=`Bot ${e.bot_id} was last seen running task ${e.task_id} (${e.task_name})`),r.c`<a target=_blank
                   rel=noopener
                   title=${i}
                   href=${Object(f.j)(e.task_id)}>${s}</a>`},uptime:(e,t)=>{const s=x(e,"uptime");return s?b.e(s):"UNKNOWN"},version:(e,t)=>{const s=e.version||"UNKNOWN";return t._verbose?s:s.substring(0,10)}};var G=s(22),K=s(36),W=s(21);const z=(e,t)=>r.c`
<th>${function(e){return j[e]||e}(e)}
  <sort-toggle .key=${e} .currentKey=${t._sort} .direction=${t._dir}>
  </sort-toggle>
</th>`,F=(e,t)=>r.c`
<tr class="bot-row ${t._botClass(e)}">
  ${t._cols.map(s=>((e,t,s)=>r.c`
<td>${y(e,t,s)}</td>`)(s,e,t))}
</tr>`,R=e=>{if(!e._primaryKey)return"";let t=e._primaryMap[e._primaryKey];return t?(t=Object(G.c)(t,e._primaryKey,e._filterQuery),s=e._primaryKey,I[s]?t.sort(c.a):t.sort(),t.map(t=>r.c`
<div class=item>
  <span class=value>${Object(m.a)(t,e._primaryKey)}</span>
  <span class=flex></span>
  <add-circle-icon-sk ?hidden=${e._filters.indexOf(Object(G.d)(e._primaryKey,t))>=0}
                      @click=${()=>e._addFilter(Object(G.d)(e._primaryKey,t))}>
  </add-circle-icon-sk>
</div>`)):r.c`
<div class=information_only>
  Hmm... no preloaded values. Maybe try typing your filter like ${e._primaryKey}:foo-bar in the
  above box and hitting enter.
</div>`;var s},q=e=>r.c`
<!-- primary key selector-->
<select-sk class="selector keys"
           @scroll=${e._scrollCheck}
           @selection-changed=${e._primaryKeyChanged}>
  ${e._filteredPrimaryArr.map(t=>((e,t)=>r.c`
<div class=item ?selected=${t._primaryKey===e}>
  <span class=key>${e}</span>
</div>`)(t,e))}
</select-sk>
<!-- secondary value selector-->
<select-sk class="selector values" disabled>
  ${R(e)}
</select-sk>`,Q=(e,t)=>r.c`
<tr>
  <td><a href=${Object(o.a)(e._makeSummaryURL(t,!0))}>${t.label}</a>:</td>
  <td>${t.value}</td>
</tr>`,X=e=>r.c`
<div class=summary ?hidden=${!e._showFleetCounts}>
  <div class="fleet_header hider title" @click=${e._toggleFleetsCount}>
    <span>Fleet</span>
    ${Object(K.a)(e._showFleetCounts)}
  </div>
  <table id=fleet_counts>
    ${e._fleetCounts.map(t=>((e,t)=>r.c`
<tr>
  <td><a href=${Object(o.a)(e._makeSummaryURL(t,!1))}>${t.label}</a>:</td>
  <td>${t.value}</td>
</tr>`)(e,t))}
  </table>
</div>

<div class=summary>
  <div class="fleet_header shower title" ?hidden=${e._showFleetCounts} @click=${e._toggleFleetsCount}>
    <span>Fleet</span>
    ${Object(K.a)(e._showFleetCounts)}
  </div>

  <div class=title>Selected</div>
  <table id=query_counts>
    ${Q(e,{label:"Displayed",value:e._bots.length})}
    ${e._queryCounts.map(t=>Q(e,t))}
  </table>
</div>`,J=e=>r.c`
<div class=header>
  <div class=filter_box ?hidden=${!e.loggedInAndAuthorized}>
    <search-icon-sk></search-icon-sk>
    <input id=filter_search class=search type=text
           placeholder='Search filters or supply a filter
                        and press enter'
           @input=${e._refilterPrimaryKeys}
           @keyup=${e._filterSearch}>
    </input>
    <!-- The following div has display:block and divides the above and
         below inline-block groups-->
    <div></div>
    ${q(e)}

    ${(e=>r.c`
<div class=options>
  <div class=verbose>
    <checkbox-sk ?checked=${e._verbose}
                 @click=${e._toggleVerbose}>
    </checkbox-sk>
    <span>Verbose Entries</span>
  </div>
  <a href=${e._matchingTasksLink()}>View Matching Tasks</a>
  <button id=delete_all
      ?disabled=${!e.permissions.delete_bot}
      @click=${e._promptMassDelete}>
    DELETE ALL DEAD BOTS
  </button>
</div>`)(e)}
  </div>

    ${X(e)}
  </div>
</div>
<div class=chip_container>
  ${e._filters.map(t=>((e,t)=>r.c`
<span class=chip>
  <span>${Object(m.c)(e)}</span>
  <cancel-icon-sk @click=${()=>t._removeFilter(e)}></cancel-icon-sk>
</span>`)(t,e))}
</div>`,Y=e=>e._showColSelector?r.c`
<!-- Stop clicks from traveling outside the popup.-->
<div class=col_selector @click=${e=>e.stopPropagation()}>
  <input id=column_search class=search type=text
         placeholder='Search columns to show'
         @input=${e._refilterPossibleColumns}
         <!-- Looking at the change event, but that had the behavior of firing
              any time the user clicked away, with seemingly no differentiation.
              Instead, we watch keyup and wait for the 'Enter' key. -->
         @keyup=${e._columnSearch}>
  </input>
  ${e._filteredPossibleColumns.map(t=>((e,t)=>r.c`
<div class=item>
  <span class=key>${e}</span>
  <span class=flex></span>
  <checkbox-sk ?checked=${t._cols.indexOf(e)>=0}
               ?disabled=${H.indexOf(e)>=0}
               @click=${s=>t._toggleCol(s,e)}
               @keypress=${s=>t._toggleCol(s,e)}>
  </checkbox-sk>
</div>`)(t,e))}
</div>`:"",Z=e=>r.c`
<swarming-app id=swapp
              client_id=${e.client_id}
              ?testing_offline=${e.testing_offline}>
  <header>
    <div class=title>Swarming Bot List</div>
      <aside class=hideable>
        <a href=/>Home</a>
        <a href=/tasklist>Task List</a>
        <a href=/bot>Bot Page</a>
        <a href=/task>Task Page</a>
      </aside>
  </header>
  <!-- Allow clicking anywhere to dismiss the column selector-->
  <main @click=${t=>e._showColSelector&&e._toggleColSelector(t)}>
    <h2 class=message ?hidden=${e.loggedInAndAuthorized}>${e._message}</h2>

    ${e.loggedInAndAuthorized?J(e):""}

    <table class=bot-table ?hidden=${!e.loggedInAndAuthorized}>
      <thead>
        <tr>
          ${(e=>r.c`
<!-- Put the click action here to make it bigger, especially for mobile.-->
<th class=col_options @click=${e._toggleColSelector}>
  <span class=show_widget>
    <more-vert-icon-sk tabindex=0 @keypress=${e._toggleColSelector}></more-vert-icon-sk>
  </span>
  <span>Bot Id</span>
  <sort-toggle @click=${e=>e.stopPropagation()&&e.preventDefault()}
               key=id .currentKey=${e._sort} .direction=${e._dir}>
  </sort-toggle>
  ${Y(e)}
</th>`)(e)}
          <!-- Slice off the first column (which is always 'id') so we can
               have a custom first box (including the widget to select columns).
            -->
          ${e._cols.slice(1).map(t=>z(t,e))}
        </tr>
      </thead>
      <tbody>${e._sortBots().map(t=>F(t,e))}</tbody>
    </table>
    <button ?hidden=${!e.loggedInAndAuthorized||!!e._filters.length||e._showAll}
            @click=${e._forceShowAll}>
      Show All
    </button>
  </main>
  <footer></footer>
  <dialog-pop-over>
    <div class='delete content'>
      <bot-mass-delete .auth_header=${e.auth_header}
                       .dimensions=${function(e){const t=Object.keys(w);return e.filter(e=>{for(const s of t)if(e.startsWith(s+":"))return!1;return!0})}(e._filters)}>
      </bot-mass-delete>
      <button class=goback tabindex=0
              @click=${e._closePopup}
              ?disabled=${e._startedDeleting&&!e._finishedDeleting}>
        ${e._startedDeleting?"DISMISS":"GO BACK - DON'T DELETE ANYTHING"}
      </button>
    </div>
  </dialog-pop-over>
</swarming-app>`;window.customElements.define("bot-list",class extends W.a{constructor(){super(Z),this._bots=[],this._cols=[],this._dir="",this._filters=[],this._limit=0,this._primaryKey="",this._showAll=!1,this._showFleetCounts=!1,this._sort="",this._verbose=!1,this._fleetCounts=E(),this._queryCounts=E(),this._stateChanged=Object(h.a)(()=>({c:this._cols,d:this._dir,e:this._showFleetCounts,f:this._filters,k:this._primaryKey,s:this._sort,show_all:this._showAll,v:this._verbose}),e=>{this._cols=e.c,e.c.length||(this._cols=["id","task","os","status"]),this._dir=e.d||"asc",this._filters=Object(m.b)(e.f),this._primaryKey=e.k,this._sort=e.s||"id",this._verbose=e.v,this._showFleetCounts=e.e,this._limit=100,this._showAll=e.show_all,this._fetch(),this.render()}),this._primaryArr=[],this._filteredPrimaryArr=[],this._possibleColumns=[],this._filteredPossibleColumns=[],this._primaryMap={},this._message="You must sign in to see anything useful.",this._showColSelector=!1,this._columnQuery="",this._filterQuery="",this._fetchController=null,this._ignoreScrolls=0}connectedCallback(){super.connectedCallback(),this._loginEvent=e=>{this._fetch(),this.render()},this.addEventListener("log-in",this._loginEvent),this._sortEvent=e=>{this._sort=e.detail.key,this._dir=e.detail.direction,this._stateChanged(),this.render()},this.addEventListener("sort-change",this._sortEvent),this._startedMassDeletingEvent=e=>{this._startedDeleting=!0,this._finishedDeleting=!1,this.render()},this.addEventListener("bots-deleting-started",this._startedMassDeletingEvent),this._finishedMassDeletingEvent=e=>{this._startedDeleting=!0,this._finishedDeleting=!0,this.render()},this.addEventListener("bots-deleting-finished",this._finishedMassDeletingEvent)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("log-in",this._loginEvent),this.removeEventListener("sort-change",this._sortEvent),this.removeEventListener("bots-deleting-started",this._startedMassDeletingEvent),this.removeEventListener("bots-deleting-finished",this._finishedMassDeletingEvent)}_addFilter(e){this._filters.indexOf(e)>=0||(this._filters.push(e),this._stateChanged(),this._bots=function(e,t){const s=[];for(const t of e){const e=t.indexOf(":"),i=t.slice(0,e),n=t.slice(e+1);s.push([i,n])}return t.filter(e=>{let t=!0;for(const i of s){const[s,n]=i;w[s]?t&=w[s](e,n):t&=-1!==v(e,s,[]).indexOf(n)}return t})}(this._filters,this._bots),this._fetch(),this.render())}_botClass(e){let t="";return e.is_dead&&(t+="dead "),e.quarantined&&(t+="quarantined "),e.maintenance_msg&&(t+="maintenance "),e.version!==this.server_details.bot_version&&(t+="old_version"),t}_closePopup(e){Object(i.b)("dialog-pop-over",this).hide(),this._startedDeleting=!1,this._finishedDeleting=!1}_columnSearch(e){if("Enter"!==e.key)return;const t=Object(i.b)("#column_search",this),s=t.value.trim();if(-1!==this._possibleColumns.indexOf(s)){if(t.value="",this._columnQuery="",-1!==this._cols.indexOf(s))return this._refilterPossibleColumns(),void Object(n.a)(`Column "${s}" already displayed.`,5e3);this._cols.push(s),this._stateChanged(),this._refilterPossibleColumns()}else Object(n.a)(`Column "${s}" is not valid.`,5e3)}_fetch(){if(!this.loggedInAndAuthorized||!this._limit)return;this._fetchController&&this._fetchController.abort(),this._fetchController=new AbortController;const e={headers:{authorization:this.auth_header},signal:this._fetchController.signal};this.app.addBusyTasks(1);let t=A(this._filters,this._limit);if(fetch(`/_ah/api/swarming/v1/bots/list?${t}`,e).then(a.a).then(s=>{this._bots=[];const i=s=>{this._bots=this._bots.concat(function(e){if(!e)return[];for(const t of e){t.state=t.state&&JSON.parse(t.state)||{};const e=t.state.disks||{},s=Object.keys(e);if(s.length){t.disks=[];for(let i=0;i<s.length;i++)t.disks.push({id:s[i],mb:e[s[i]].free_mb});t.disks.sort((function(e,t){return t.mb-e.mb}))}else t.disks=[{id:"unknown",mb:0}];t.state.temp=g(t.state.temp);const i=[],n=t&&t.state&&t.state.devices||{};for(const e in n){const s=n[e];s.serial=e,s.okay="available"===s.state;const r=k(t,"device_type")||["UNKNOWN"];s.device_type=r[0],s.temp=g(s.temp),i.push(s)}i.sort((e,t)=>e.serial<t.serial?-1:e.serial>t.serial?1:0),t.state.devices=i;for(const e of O)Object(f.h)(t,e)}return e}(s.items)),this.render(),(this._filters.length||this._showAll)&&s.cursor?(this._limit=200,t=A(this._filters,this._limit,s.cursor),fetch(`/_ah/api/swarming/v1/bots/list?${t}`,e).then(a.a).then(i).catch(e=>this.fetchError(e,"bots/list (paging)"))):this.app.finishedTask()};i(s)}).catch(e=>this.fetchError(e,"bots/list")),this.app.addBusyTasks(1),fetch("/_ah/api/swarming/v1/bots/count?"+t,e).then(a.a).then(e=>{this._queryCounts=N(this._queryCounts,e),this.render(),this.app.finishedTask()}).catch(e=>this.fetchError(e,"bots/count (query)")),this._fleetCounts._queried||(this._fleetCounts._queried=!0,this.app.addBusyTasks(1),fetch("/_ah/api/swarming/v1/bots/count",e).then(a.a).then(e=>{this._fleetCounts=N(this._fleetCounts,e),this.render(),this.app.finishedTask()}).catch(e=>this.fetchError(e,"bots/count (fleet)"))),!this._fetchedDimensions){this._fetchedDimensions=!0,this.app.addBusyTasks(1);const e={headers:{authorization:this.auth_header}};fetch("/_ah/api/swarming/v1/bots/dimensions",e).then(a.a).then(e=>{this._primaryMap=function(e){var t={};(e=e||[]).forEach((function(e){L.indexOf(e.key)>=0||(t[e.key]=e.value)})),t.android_devices&&t.android_devices.push("0");for(const e of $)t[e]&&-1===t[e].indexOf("none")&&t[e].push("none");return t.id=null,t.task=["busy","idle"],t.status=["alive","dead","quarantined","maintenance"],t}(e.bots_dimensions),this._possibleColumns=function(e){if(!e)return[];const t=[];return e.forEach((function(e){-1===L.indexOf(e.key)&&t.push(e.key)})),t.push("id"),Array.prototype.push.apply(t,S),t.sort(),t}(e.bots_dimensions),this._filteredPossibleColumns=this._possibleColumns.slice(),this._primaryArr=Object.keys(this._primaryMap),this._primaryArr.sort(),this._filteredPrimaryArr=this._primaryArr.slice(),this._refilterPossibleColumns(),this.app.finishedTask()}).catch(e=>this.fetchError(e,"bots/dimensions"))}}_filterSearch(e){if("Enter"!==e.key)return;const t=Object(i.b)("#filter_search",this),s=t.value.trim();if(-1!==s.indexOf(":")){if(t.value="",this._filterQuery="",this._primaryKey="",-1!==this._filters.indexOf(s))return this._refilterPrimaryKeys(),void Object(n.a)(`Filter "${s}" is already active`,5e3);this._addFilter(s),this._refilterPrimaryKeys()}else Object(n.a)('Invalid filter.  Should be like "foo:bar"',5e3)}_forceShowAll(){this._showAll=!0,this._stateChanged(),this._fetch()}_makeSummaryURL(e,t){if(!e||"Displayed"===e.label||"All"===e.label)return;const s=e.label.toLowerCase();let i="status:"+s;"busy"!==s&&"idle"!==s||(i="task:"+s);const n=new URL(window.location.href);if(t){if(-1!==n.searchParams.getAll("f").indexOf(i))return;return n.searchParams.append("f",i),n.href}const r={s:[this._sort],c:this._cols,v:[this._verbose],f:[i],e:[!0]};return n.pathname+"?"+d.b(r)}_matchingTasksLink(){const e=["name","state","created_ts"],t=this._filters.filter(e=>!w[e.split(":")[0]]);for(const s of t){const t=s.split(":",1)[0];-1===e.indexOf(t)&&e.push(t)}return Object(f.i)(t,e)}_primaryKeyChanged(e){this._primaryKey=this._filteredPrimaryArr[e.detail.selection],this._stateChanged(),this.render()}_promptMassDelete(e){Object(i.b)("bot-mass-delete",this).show(),Object(i.b)("dialog-pop-over",this).show(),Object(i.b)("dialog-pop-over button.goback",this).focus()}_refilterPossibleColumns(e){const t=Object(i.b)("#column_search",this);this._columnQuery=t&&t.value||"",this._filteredPossibleColumns=Object(G.a)(this._possibleColumns,this._columnQuery),function(e,t){const s={};for(const e of t)s[e]=!0;e.sort((e,t)=>{const i=s[e],n=s[t];return i&&!n?-1:n&&!i?1:i&&n?T(e,t):e.localeCompare(t)})}(this._filteredPossibleColumns,this._cols),this.render()}_refilterPrimaryKeys(e){this._filterQuery=Object(i.b)("#filter_search",this).value,this._filteredPrimaryArr=Object(G.b)(this._primaryArr,this._primaryMap,this._filterQuery),this._filterQuery&&this._filteredPrimaryArr.length>0&&-1===this._filteredPrimaryArr.indexOf(this._primaryKey)&&(this._primaryKey=this._filteredPrimaryArr[0],this._stateChanged()),this.render()}_removeFilter(e){const t=this._filters.indexOf(e);-1!==t&&(this._filters.splice(t,1),this._stateChanged(),this._fetch(),this.render())}render(){this._cols.sort(T),super.render(),this._scrollToPrimaryKey()}_scrollCheck(){this._ignoreScrolls>0?this._ignoreScrolls--:this._humanScrolledKeys=!0}_scrollToPrimaryKey(){const e=Object(i.b)(".keys.selector",this);if(this._primaryKey&&!this._humanScrolledKeys&&e){const t=Object(i.b)(".item[selected]",e);t&&(this._ignoreScrolls++,e.scrollTo({top:t.offsetTop-160}))}}_sortBots(){return this._bots.sort((e,t)=>{const s=this._sort;if(!s)return 0;let i=1;"desc"===this._dir&&(i=-1);const n=V[s];if(n)return n(i,e,t);let r=y(s,e,this);"none"===r&&(r="zzz");let o=y(s,t,this);return"none"===o&&(o="zzz"),i*c()(r,o)}),this._bots}_toggleCol(e,t){if(H.indexOf(t)>=0)return;e.preventDefault(),e.stopPropagation();const s=this._cols.indexOf(t);s>=0?this._cols.splice(s,1):this._cols.push(t),this._refilterPossibleColumns(),this._stateChanged(),this.render()}_toggleColSelector(e){e.preventDefault(),e.stopPropagation(),this._showColSelector=!this._showColSelector,this._refilterPossibleColumns()}_toggleFleetsCount(e){e.preventDefault(),e.stopPropagation(),this._showFleetCounts=!this._showFleetCounts,this._stateChanged(),this.render()}_toggleVerbose(e){e.preventDefault(),this._verbose=!this._verbose,this._stateChanged(),this.render()}});s(51)}]);