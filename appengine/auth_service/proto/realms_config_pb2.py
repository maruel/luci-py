# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: realms_config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='realms_config.proto',
  package='auth_service',
  syntax='proto3',
  serialized_options=b'Z/go.chromium.org/luci/common/proto/realms;realms',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13realms_config.proto\x12\x0c\x61uth_service\"`\n\tRealmsCfg\x12#\n\x06realms\x18\x01 \x03(\x0b\x32\x13.auth_service.Realm\x12.\n\x0c\x63ustom_roles\x18\x02 \x03(\x0b\x32\x18.auth_service.CustomRole\"k\n\x05Realm\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x65xtends\x18\x02 \x03(\t\x12\'\n\x08\x62indings\x18\x03 \x03(\x0b\x32\x15.auth_service.Binding\x12\x1a\n\x12\x65nforce_in_service\x18\x04 \x03(\t\"+\n\x07\x42inding\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x12\n\nprincipals\x18\x02 \x03(\t\"@\n\nCustomRole\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x65xtends\x18\x02 \x03(\t\x12\x13\n\x0bpermissions\x18\x03 \x03(\tB1Z/go.chromium.org/luci/common/proto/realms;realmsb\x06proto3'
)




_REALMSCFG = _descriptor.Descriptor(
  name='RealmsCfg',
  full_name='auth_service.RealmsCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='realms', full_name='auth_service.RealmsCfg.realms', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='custom_roles', full_name='auth_service.RealmsCfg.custom_roles', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=133,
)


_REALM = _descriptor.Descriptor(
  name='Realm',
  full_name='auth_service.Realm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='auth_service.Realm.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extends', full_name='auth_service.Realm.extends', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bindings', full_name='auth_service.Realm.bindings', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enforce_in_service', full_name='auth_service.Realm.enforce_in_service', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=242,
)


_BINDING = _descriptor.Descriptor(
  name='Binding',
  full_name='auth_service.Binding',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='role', full_name='auth_service.Binding.role', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='principals', full_name='auth_service.Binding.principals', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=244,
  serialized_end=287,
)


_CUSTOMROLE = _descriptor.Descriptor(
  name='CustomRole',
  full_name='auth_service.CustomRole',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='auth_service.CustomRole.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extends', full_name='auth_service.CustomRole.extends', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='permissions', full_name='auth_service.CustomRole.permissions', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=289,
  serialized_end=353,
)

_REALMSCFG.fields_by_name['realms'].message_type = _REALM
_REALMSCFG.fields_by_name['custom_roles'].message_type = _CUSTOMROLE
_REALM.fields_by_name['bindings'].message_type = _BINDING
DESCRIPTOR.message_types_by_name['RealmsCfg'] = _REALMSCFG
DESCRIPTOR.message_types_by_name['Realm'] = _REALM
DESCRIPTOR.message_types_by_name['Binding'] = _BINDING
DESCRIPTOR.message_types_by_name['CustomRole'] = _CUSTOMROLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RealmsCfg = _reflection.GeneratedProtocolMessageType('RealmsCfg', (_message.Message,), {
  'DESCRIPTOR' : _REALMSCFG,
  '__module__' : 'realms_config_pb2'
  # @@protoc_insertion_point(class_scope:auth_service.RealmsCfg)
  })
_sym_db.RegisterMessage(RealmsCfg)

Realm = _reflection.GeneratedProtocolMessageType('Realm', (_message.Message,), {
  'DESCRIPTOR' : _REALM,
  '__module__' : 'realms_config_pb2'
  # @@protoc_insertion_point(class_scope:auth_service.Realm)
  })
_sym_db.RegisterMessage(Realm)

Binding = _reflection.GeneratedProtocolMessageType('Binding', (_message.Message,), {
  'DESCRIPTOR' : _BINDING,
  '__module__' : 'realms_config_pb2'
  # @@protoc_insertion_point(class_scope:auth_service.Binding)
  })
_sym_db.RegisterMessage(Binding)

CustomRole = _reflection.GeneratedProtocolMessageType('CustomRole', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMROLE,
  '__module__' : 'realms_config_pb2'
  # @@protoc_insertion_point(class_scope:auth_service.CustomRole)
  })
_sym_db.RegisterMessage(CustomRole)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
