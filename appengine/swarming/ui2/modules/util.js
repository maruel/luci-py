// Copyright 2018 The LUCI Authors. All rights reserved.
// Use of this source code is governed under the Apache License, Version 2.0
// that can be found in the LICENSE file.

/** @module swarming-ui/util
 * @description
 *
 * <p>
 *  A general set of useful functions.
 * </p>
 */

/** Performs an in-place, stable sort on the passed-in array using
 * the passed in comparison function for all non-null and non-undefined
 * elements.
 * @param {Array} arr - The array to sort.
 * @param {Function} comp - A function that compares two elements
 *                   in the array and returns an integer indicating
 *                   whether a is greater than, less than or equal to b.
 */
export function stableSort(arr, comp) {
  if (!arr || !comp) {
    console.warn('missing arguments to stableSort', arr, comp);
    return;
  }
  // We can guarantee a potential non-stable sort (like V8's
  // Array.prototype.sort()) to be stable by first storing the index in the
  // original sorting and using that if the original compare was 0.
  arr.forEach((e, i) => {
    if (e !== undefined && e !== null) {
      e.__sortIdx = i;
    }
  });

  arr.sort((a, b) => {
    // undefined and null elements always go last.
    if (a === undefined || a === null) {
      if (b === undefined || b === null) {
        return 0;
      }
      return 1;
    }
    if (b === undefined || b === null) {
      return -1;
    }
    let c = comp(a, b);
    if (c === 0) {
      return a.__sortIdx - b.__sortIdx;
    }
    return c;
  });
}

// sanitizeAndHumanizeTime parses a date string or ms_since_epoch into a JS
// Date object, assuming UTC time. It also creates a human readable form in
// the obj under a key with a human_ prefix.  E.g.
// swarming.sanitizeAndHumanizeTime(foo, 'some_ts')
// parses the string/int at foo['some_ts'] such that foo['some_ts'] is now a
// Date object and foo['human_some_ts'] is the human formated version from
// sk.human.localeTime.
export function sanitizeAndHumanizeTime(obj, key) {
  obj['human_'+key] = '‑‑';
  if (obj[key]) {
    if (obj[key].endsWith && !obj[key].endsWith('Z')) {
      // Timestamps from the server are missing the 'Z' that specifies Zulu
      // (UTC) time. If that's not the case, add the Z. Otherwise, some
      // browsers interpret this as local time, which throws off everything.
      // TODO(kjlubick): Should the server output milliseconds since the
      // epoch?  That would be more consistent.
      // See http://crbug.com/714599
      obj[key] += 'Z';
    }
    obj[key] = new Date(obj[key]);

    // Extract the timezone.
    var str = obj[key].toString();
    var timezone = str.substring(str.indexOf('('));

    // If timestamp is today, skip the date.
    var now = new Date();
    if (obj[key].getDate() == now.getDate() &&
        obj[key].getMonth() == now.getMonth() &&
        obj[key].getYear() == now.getYear()) {
      obj['human_'+key] = obj[key].toLocaleTimeString() + ' ' + timezone;
    } else {
      obj['human_'+key] = obj[key].toLocaleString() + ' ' + timezone;
    }
  }
}