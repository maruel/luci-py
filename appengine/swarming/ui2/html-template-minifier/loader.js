// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

const UglifyJS = require("uglify-es");

module.exports = function minifyHTMLInTemplates(source) {
  //console.log("top of loader")
  // pre-minify the js (mainly to remove comments)
  let result = UglifyJS.minify(source);
  if (result.error) {
    console.log('Could not minify html: ', result.error);
    return source;
  }
  source = result.code

  let minified = '';
  let idx = 0;
  while (idx < source.length) {
    let m = source.indexOf('html`', idx);
    if (m === -1) {
      // no other templates, append everything else.
      minified += source.slice(idx);
      break;
    }
    let end = source.indexOf('`', m+5);
    if (end === -1) {
      // malformed string literals, bail out
      console.log('bailing out')
      return source;
    }
    let t = source.slice(m+5, end);
    minified += source.slice(idx, m);
    minified += 'html`';
    minified += minifyTemplate(t);
    minified += '`';
    idx = end+1;
  }
  return minified;
}

const IGNORE_PAIRS=['<pre', '</pre>', '${', '}'];

function minifyTemplate(t) {
  let idx = 0;
  let minified = '';

  let safety = 100;
  while (idx < t.length) {
    let nextIgnoreIdx = t.length;
    let nextEndIgnore = '';
    for (let i = 0; i < IGNORE_PAIRS.length; i+=2) {
      let ignoreStart = IGNORE_PAIRS[i];
      let ignoreIdx = t.indexOf(ignoreStart, idx);
      if (ignoreIdx !== -1 && ignoreIdx < nextIgnoreIdx) {
        nextIgnoreIdx = ignoreIdx+ignoreStart.length;
        nextEndIgnore = IGNORE_PAIRS[i+1];
      }
    }

    let nextEndIgnoreIdx = 0;
    if (nextIgnoreIdx === -1) {
      nextIgnoreIdx = t.length;
      nextEndIgnoreIdx = t.length;
    } else {
      nextEndIgnoreIdx = t.indexOf(nextEndIgnore, nextIgnoreIdx);
    }
    // nextIgnoreIdx is set to where we can safely minify to.
    // nextEndIgnoreIdx is where we will pick up next loop.

    // For now, the only minifying we do is reduce whitespace and
    // remove comments
    let segment = t.slice(idx, nextIgnoreIdx);
    segment = segment.replace(/\s+/g, ' ');
    segment = segment.replace(/\<!--.+?--\>/, '');

    minified += segment;
    minified += t.slice(nextIgnoreIdx, nextEndIgnoreIdx+nextEndIgnore.length);
    idx = nextEndIgnoreIdx+nextEndIgnore.length;
    safety--;
    if (safety < 0) {
      break;
    }
  }
  return minified;
}