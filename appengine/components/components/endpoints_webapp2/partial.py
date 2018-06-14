# Copyright 2018 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Partial response utilities for an Endpoints v1 over webapp2 service.

Grammar of a fields partial response string:
   fields: selector [,selector]*
 selector: path [(fields)]?
     path: name [/name]*
     name: [A-Za-z_][A-Za-z0-9_]* | \*

Examples:

fields=a
Response includes the value of the "a" field.

fields=a,b
Response includes the values of the "a" and "b" fields.

fields=a/b
Response includes the value of the "b" field of "a". If "a" is an array,
response includes the values of the "b" fields of every element in the array.

fields=a/*/c
For every element or field of "a", response includes the value of that element
or field's "c" field.

fields=a(b,c)
Equivalent to fields=a/b union fields=a/c.
"""


class ParsingError(Exception):
  """Indicates an error during parsing.

  Fields:
    index: The index the error occurred at.
    message: The error message.
  """

  def __init__(self, index, message):
    super(ParsingError, self).__init__('%d: %s' % (index, message))
    self.index = index
    self.message = message


def _merge(source, destination):
  """Recursively merges the source dict into the destination dict.

  Args:
    source: A dict whose values are source dicts.
    destination: A dict whose values are destination dicts.
  """
  for key, value in source.iteritems():
    if destination.get(key):
      _merge(value, destination[key])
    else:
      destination[key] = value


class _ParsingContext(object):
  """Encapsulates parsing information.

  Attributes:
    accumulator: A list of field name characters accumulated so far.
    expecting_name: Whether or not a field name is expected.
    fields: A dict of accumulated fields.
  """

  def __init__(self):
    """Initializes a new instance of ParsingContext."""
    # Used to accumulate field names.
    self.accumulator = []
    # Pointer to the subfield dict of the last added field.
    self._last = None
    self.expecting_name = True
    self.fields = {}

  def accumulate(self, char):
    """Accumulates the given char.

    Args:
      char: The character to accumulate.
    """
    # Accumulate all characters even if they aren't allowed by the grammar.
    # In the worst case there will be extra keys in the fields dict which will
    # be ignored when the mask is applied because they don't match any legal
    # field name. It won't cause incorrect masks to be applied. The exceptions
    # are / and * which have special meaning. See add_field below.
    self.accumulator.append(char)

  def add_field(self, i):
    """Records the field name in the accumulator then clears the accumulator.

    Args:
      i: The index the parser is at.
    """
    # TODO(smut): Handle * special case.
    if not self.accumulator:
      raise ParsingError(i, 'expected name')

    # / has special meaning; a/b/c is shorthand for a(b(c)). Add subfield dicts
    # recursively. E.g. if the fields dict is empty then parsing a/b/c is like
    # setting fields["a"] = {"b": {"c": {}} and pointing last to c's value.
    pointer = self.fields
    for part in ''.join(self.accumulator).split('/'):
      if not part:
        raise ParsingError(i, 'empty name in path')
      pointer = pointer.setdefault(part, {})

    self._last = pointer
    self.accumulator = []

  def add_subfields(self, subfields):
    """Adds the given subfields to the last added field.

    Args:
      subfields: A dict of accumulated subfields.

    Returns:
      False if there was no last added field to add subfields to, else True.
    """
    if self._last is None:
      return False
    _merge(subfields, self._last)
    return True


def _parse(fields):
  """Parses the given partial response string into a partial response mask.

  Args:
    fields: A fields partial response string.

  Returns:
    A dict which can be used to mask a JSON response.
  """
  stack = [_ParsingContext()]

  i = 0
  while i < len(fields):
    # Invariants maintained below.
    # Stack invariant: The stack always has at least one context.
    assert stack, fields
    # Accumulator invariant: Non-empty accumulator implies expecting a name.
    assert not stack[-1].accumulator or stack[-1].expecting_name, fields

    if fields[i] == ',':
      # If we just returned from a lower context, no name is expected.
      if stack[-1].expecting_name:
        stack[-1].add_field(i)
      stack[-1].expecting_name = True

    elif fields[i] == '(':
      # Maintain accumulator invariant.
      # A name must occur before any (.
      stack[-1].add_field(i)
      stack[-1].expecting_name = False

      # Enter a new context. When we return from this context we don't expect to
      # accumulate another name. There must be , or a return to a higher context
      # (or the end of the string altogether).
      stack.append(_ParsingContext())

    elif fields[i] == ')':
      # If we just returned from a lower context, no name is expected.
      if stack[-1].expecting_name:
        stack[-1].add_field(i)

      # Return to a higher context. Maintain stack invariant.
      subfields = stack.pop().fields
      if not stack:
        # Mismatched ().
        raise ParsingError(i, 'unexpected )')

      # See accumulator invariant maintenance above.
      assert not stack[-1].expecting_name, fields

      if not stack[-1].add_subfields(subfields):
        # ) before any field.
        raise ParsingError(i, 'unexpected (')

    else:
      # If we just returned from a lower context, no name is expected.
      if not stack[-1].expecting_name:
        raise ParsingError(i, 'unexpected name')
      stack[-1].accumulate(fields[i])

    i += 1

  if len(stack) != 1:
    # Mismatched ().
    raise ParsingError(i, 'expected )')

  # If we just returned from a lower context, no name is expected.
  if stack[-1].expecting_name:
    stack[-1].add_field(i)

  return stack[0].fields
