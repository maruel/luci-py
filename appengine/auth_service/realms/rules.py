# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Expansion of realms_config.Realm into a flat form."""

import collections

from components.auth.proto import realms_pb2
from components.config import validation as cfg_validation

from proto import realms_config_pb2

from realms import common
from realms import permissions
from realms import validation


def expand_realms(db, project_id, realms_cfg):
  """Expands realms_config_pb2.RealmsCfg into a flat realms_pb2.Realms.

  The returned realms_pb2.Realms contains realms and permissions of a single
  project only. Permissions not mentioned in the project's realms are omitted.
  All realms_pb2.Permission messages have names only (no metadata). api_version
  field is omitted.

  All such realms_pb2.Realms messages across all projects (plus a list of all
  defined permissions with all their metadata) are later merged together into
  a final universal realms_pb2.Realms by realms.merge(...) in
  components/auth/replication.py.

  Args:
    db: a permissions.DB instance with current permissions and roles.
    project_id: ID of a LUCI project to use as a prefix in realm names.
    realms_cfg: an instance of realms_config_pb2.RealmsCfg to expand.

  Returns:
    realms_pb2.Realms with expanded realms (with caveats mentioned above).

  Raises:
    ValueError if the validation fails.
  """
  # `internal` is True when expanding internal realms (defined in a service
  # config file). Such realms can use internal roles and permissions and they
  # do not have implicit root bindings (since they are not associated with
  # any "project:<X>" identity used in implicit root bindings).
  internal = project_id == common.INTERNAL_PROJECT

  # The server code could have changed since the config passed the validation
  # and realms_cfg may not be valid anymore. Verify it still is. The code below
  # depends crucially on the validity of realms_cfg.
  validation.Validator(
      cfg_validation.Context.raise_on_error(), db, internal,
  ).validate(realms_cfg)

  # A lazily populated {role -> tuple of permissions} mapping.
  roles_expander = RolesExpander(db.roles, realms_cfg.custom_roles)
  # A helper to traverse the realms graph.
  realms_expander = RealmsExpander(roles_expander, realms_cfg.realms)

  # This creates @root realm and (optionally) extends it with implicit bindings.
  realms_expander.extend_root(
      db.implicit_root_bindings(project_id) if not internal else [])

  # Visit all realms and build preliminary bindings as pairs of
  # (a tuple with permission indexes, a list of principals who have them). The
  # bindings are preliminary since we don't know final permission indexes yet
  # and instead use some internal indexes as generated by RolesExpander. We
  # need to finish this first pass to gather the list of ALL used permissions,
  # so we can calculate final indexes. This is done inside of `roles_expander`.
  realms = []  # [(name, (permissions tuple, principals list))]
  for name in realms_expander.realm_names:
    # Build a mapping from a principal to the permissions set they have.
    principal_to_perms = collections.defaultdict(set)
    for principal, perms in realms_expander.per_principal_bindings(name):
      principal_to_perms[principal].update(perms)
    # Combine entries with the same set of permissions into one.
    perms_to_principals = collections.defaultdict(list)
    for principal, perms in principal_to_perms.items():
      perms_to_principals[tuple(sorted(perms))].append(principal)
    realms.append((name, perms_to_principals.items()))

  # We now know all permissions ever used by all realms. Convert them into the
  # form suitable for realm_pb2 by sorting alphabetically. Keep the mapping
  # between old and new indexes, to be able to change indexes in permission
  # tuples we stored in `realms`.
  perms, index_map = roles_expander.sorted_permissions()

  # Build the final sorted form of all realms by relabeling permissions
  # according to the index_map and by sorting stuff.
  return realms_pb2.Realms(
      permissions=[realms_pb2.Permission(name=p) for p in perms],
      realms=[
          realms_pb2.Realm(
              name='%s:%s' % (project_id, name),
              bindings=to_normalized_bindings(perms_to_principals, index_map),
              data=realms_expander.realm_data(name),
          )
          for name, perms_to_principals in realms
      ])


class RolesExpander(object):
  """Keeps track of permissions and `role => [permission]` expansions.

  Permissions are represented internally as integers to speed up set operations.
  The mapping from a permission to a corresponding integer is lazily built and
  should be considered arbitrary (it depends on the order of method calls). But
  it doesn't matter since in the end we relabel all permissions according to
  their indexes in the final sorted list of permissions.

  Should be used only with validated realms_config_pb2.RealmsCfg, may cause
  stack overflow or raise random exceptions otherwise.
  """

  def __init__(self, builtin_roles, custom_roles):
    self._builtin_roles = builtin_roles
    self._custom_roles = {r.name: r for r in custom_roles}
    self._permissions = {}  # permission name => its index
    self._roles = {}  # role name => set indexes of permissions

  def _perm_index(self, name):
    """Returns an internal index that represents the given permission string."""
    idx = self._permissions.get(name)
    if idx is None:
      idx = len(self._permissions)
      self._permissions[name] = idx
    return idx

  def _perm_indexes(self, iterable):
    """Yields indexes of given permission strings."""
    return (self._perm_index(p) for p in iterable)

  def role(self, role):
    """Returns an unsorted tuple of indexes of permissions of the role."""
    perms = self._roles.get(role)
    if perms is not None:
      return perms

    if role.startswith(permissions.BUILTIN_ROLE_PREFIX):
      perms = self._perm_indexes(self._builtin_roles[role].permissions)
    elif role.startswith(permissions.CUSTOM_ROLE_PREFIX):
      custom_role = self._custom_roles[role]
      perms = set(self._perm_indexes(custom_role.permissions))
      for parent in custom_role.extends:
        perms.update(self.role(parent))
    else:
      raise AssertionError('Impossible role %s' % (role,))

    perms = tuple(perms)
    self._roles[role] = perms
    return perms

  def sorted_permissions(self):
    """Returns a sorted list of permission and a old->new index mapping list.

    See to_normalized_bindings below for how it is used.
    """
    perms = sorted(self._permissions)
    mapping = [None]*len(perms)
    for new_idx, p in enumerate(perms):
      old_idx = self._permissions[p]
      mapping[old_idx] = new_idx
    assert all(v is not None for v in mapping), mapping
    return perms, mapping


class RealmsExpander(object):
  """Helper to traverse the realm inheritance graph."""

  def __init__(self, roles, realms):
    self._roles = roles
    self._realms = {r.name: r for r in realms}
    self._data = {}  # name -> realms_pb2.RealmData, memoized

  @staticmethod
  def _parents(realm):
    """Given a realms_config_pb2.Realm yields names of immediate parents."""
    if realm.name == common.ROOT_REALM:
      return
    yield common.ROOT_REALM
    for name in realm.extends:
      if name != common.ROOT_REALM:
        yield name

  def extend_root(self, bindings):
    """Adds the given list of realms_config_pb2.Binding to the root realm."""
    root = realms_config_pb2.Realm(name=common.ROOT_REALM)
    if common.ROOT_REALM in self._realms:
      root.CopyFrom(self._realms[common.ROOT_REALM])
    root.bindings.extend(bindings)
    self._realms[common.ROOT_REALM] = root

  @property
  def realm_names(self):
    """Returns a sorted list of names of all realms, always including @root."""
    return sorted(self._realms)

  def per_principal_bindings(self, realm):
    """Yields pairs of (a single principal, permissions tuple) in the realm.

    Returns a lot of duplicates. It's the caller's job to skip them.
    """
    r = self._realms[realm]
    assert r.name == realm

    for b in r.bindings:
      perms = self._roles.role(b.role)  # the tuple of permissions of the role
      for principal in b.principals:
        yield principal, perms

    for parent in self._parents(r):
      for principal, perms in self.per_principal_bindings(parent):
        yield principal, perms

  def realm_data(self, name):
    """Returns calculated realms_pb2.RealmData for a realm."""
    if name not in self._data:
      realm = self._realms[name]
      extends = [self.realm_data(p) for p in self._parents(realm)]
      self._data[name] = derive_realm_data(realm, [x for x in extends if x])
    return self._data[name]


def to_normalized_bindings(perms_to_principals, index_map):
  """Produces a sorted list of realms_pb2.Binding.

  Bindings are given as a list of (tuple of permissions, list of principals)
  pairs. Permissions are specified through their internal indexes as produced
  by RolesExpander. We convert them into "public" ones (the ones that correspond
  to the sorted permissions list in the realms_pb2.Realms proto). The mapping
  from an old to a new index is given by `new = index_map[old]`.

  Args:
    perms_to_principals: a list of (tuple of permissions, list of principals).
    index_map: defines how to remap permission indexes (old -> new).

  Returns:
    A sorted list of realm_pb2.Binding.
  """
  normalized = (
      (sorted(index_map[idx] for idx in perms), sorted(principals))
      for perms, principals in perms_to_principals
  )
  return [
      realms_pb2.Binding(permissions=perms, principals=principals)
      for perms, principals in sorted(normalized, key=lambda x: x[0])
  ]


def derive_realm_data(realm, extends):
  """Calculates realms_pb2.RealmData from the realm config and parent data.

  Args:
    realm: realms_config_pb2.Realm to calculate the data for.
    extends: a list of realms_pb2.RealmData it extends from.

  Returns:
    realms_pb2.RealmData or None if empty.
  """
  enforce_in_service = set(realm.enforce_in_service)
  for d in extends:
    enforce_in_service.update(d.enforce_in_service)
  if not enforce_in_service:
    return None
  return realms_pb2.RealmData(enforce_in_service=sorted(enforce_in_service))
