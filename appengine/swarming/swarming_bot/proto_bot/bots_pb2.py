# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bots.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import status_pb2 as status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='bots.proto',
  package='google.devtools.remoteworkers.v1test2',
  syntax='proto3',
  serialized_pb=_b('\n\nbots.proto\x12%google.devtools.remoteworkers.v1test2\x1a\x19google/protobuf/any.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0cstatus.proto\"\xab\x02\n\nBotSession\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x62ot_id\x18\x02 \x01(\t\x12@\n\x06status\x18\x03 \x01(\x0e\x32\x30.google.devtools.remoteworkers.v1test2.BotStatus\x12=\n\x06worker\x18\x04 \x01(\x0b\x32-.google.devtools.remoteworkers.v1test2.Worker\x12<\n\x06leases\x18\x05 \x03(\x0b\x32,.google.devtools.remoteworkers.v1test2.Lease\x12/\n\x0b\x65xpire_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07version\x18\x07 \x01(\t\"\xa8\x02\n\x05Lease\x12\x12\n\nassignment\x18\x01 \x01(\t\x12@\n\x05state\x18\x02 \x01(\x0e\x32\x31.google.devtools.remoteworkers.v1test2.LeaseState\x12\"\n\x06status\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12\x43\n\x0crequirements\x18\x04 \x01(\x0b\x32-.google.devtools.remoteworkers.v1test2.Worker\x12/\n\x0b\x65xpire_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x11inline_assignment\x18\x06 \x01(\x0b\x32\x14.google.protobuf.Any\"\xbc\x01\n\x06Worker\x12>\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32-.google.devtools.remoteworkers.v1test2.Device\x12J\n\nproperties\x18\x02 \x03(\x0b\x32\x36.google.devtools.remoteworkers.v1test2.Worker.Property\x1a&\n\x08Property\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x8c\x01\n\x06\x44\x65vice\x12\x0e\n\x06handle\x18\x01 \x01(\t\x12J\n\nproperties\x18\x02 \x03(\x0b\x32\x36.google.devtools.remoteworkers.v1test2.Device.Property\x1a&\n\x08Property\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\xc5\x01\n\tAdminTemp\x12I\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x38.google.devtools.remoteworkers.v1test2.AdminTemp.Command\x12\x0b\n\x03\x61rg\x18\x02 \x01(\t\"`\n\x07\x43ommand\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0e\n\nBOT_UPDATE\x10\x01\x12\x0f\n\x0b\x42OT_RESTART\x10\x02\x12\x11\n\rBOT_TERMINATE\x10\x03\x12\x10\n\x0cHOST_RESTART\x10\x04\"q\n\x17\x43reateBotSessionRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12\x46\n\x0b\x62ot_session\x18\x02 \x01(\x0b\x32\x31.google.devtools.remoteworkers.v1test2.BotSession\"\xa0\x01\n\x17UpdateBotSessionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x46\n\x0b\x62ot_session\x18\x02 \x01(\x0b\x32\x31.google.devtools.remoteworkers.v1test2.BotSession\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\xb5\x01\n\x17PostBotEventTempRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12Q\n\x04type\x18\x02 \x01(\x0e\x32\x43.google.devtools.remoteworkers.v1test2.PostBotEventTempRequest.Type\x12\x0b\n\x03msg\x18\x03 \x01(\t\",\n\x04Type\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04INFO\x10\x01\x12\t\n\x05\x45RROR\x10\x02*g\n\tBotStatus\x12\x1a\n\x16\x42OT_STATUS_UNSPECIFIED\x10\x00\x12\x06\n\x02OK\x10\x01\x12\r\n\tUNHEALTHY\x10\x02\x12\x12\n\x0eHOST_REBOOTING\x10\x03\x12\x13\n\x0f\x42OT_TERMINATING\x10\x04*`\n\nLeaseState\x12\x1b\n\x17LEASE_STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\r\n\tCOMPLETED\x10\x04\x12\r\n\tCANCELLED\x10\x05\x32\x82\x03\n\x04\x42ots\x12\x85\x01\n\x10\x43reateBotSession\x12>.google.devtools.remoteworkers.v1test2.CreateBotSessionRequest\x1a\x31.google.devtools.remoteworkers.v1test2.BotSession\x12\x85\x01\n\x10UpdateBotSession\x12>.google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest\x1a\x31.google.devtools.remoteworkers.v1test2.BotSession\x12j\n\x10PostBotEventTemp\x12>.google.devtools.remoteworkers.v1test2.PostBotEventTempRequest\x1a\x16.google.protobuf.Emptyb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,status__pb2.DESCRIPTOR,])

_BOTSTATUS = _descriptor.EnumDescriptor(
  name='BotStatus',
  full_name='google.devtools.remoteworkers.v1test2.BotStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BOT_STATUS_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OK', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNHEALTHY', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOST_REBOOTING', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOT_TERMINATING', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1787,
  serialized_end=1890,
)
_sym_db.RegisterEnumDescriptor(_BOTSTATUS)

BotStatus = enum_type_wrapper.EnumTypeWrapper(_BOTSTATUS)
_LEASESTATE = _descriptor.EnumDescriptor(
  name='LeaseState',
  full_name='google.devtools.remoteworkers.v1test2.LeaseState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEASE_STATE_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PENDING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACTIVE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMPLETED', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANCELLED', index=4, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1892,
  serialized_end=1988,
)
_sym_db.RegisterEnumDescriptor(_LEASESTATE)

LeaseState = enum_type_wrapper.EnumTypeWrapper(_LEASESTATE)
BOT_STATUS_UNSPECIFIED = 0
OK = 1
UNHEALTHY = 2
HOST_REBOOTING = 3
BOT_TERMINATING = 4
LEASE_STATE_UNSPECIFIED = 0
PENDING = 1
ACTIVE = 2
COMPLETED = 4
CANCELLED = 5


_ADMINTEMP_COMMAND = _descriptor.EnumDescriptor(
  name='Command',
  full_name='google.devtools.remoteworkers.v1test2.AdminTemp.Command',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOT_UPDATE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOT_RESTART', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOT_TERMINATE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOST_RESTART', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1227,
  serialized_end=1323,
)
_sym_db.RegisterEnumDescriptor(_ADMINTEMP_COMMAND)

_POSTBOTEVENTTEMPREQUEST_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='google.devtools.remoteworkers.v1test2.PostBotEventTempRequest.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1741,
  serialized_end=1785,
)
_sym_db.RegisterEnumDescriptor(_POSTBOTEVENTTEMPREQUEST_TYPE)


_BOTSESSION = _descriptor.Descriptor(
  name='BotSession',
  full_name='google.devtools.remoteworkers.v1test2.BotSession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.devtools.remoteworkers.v1test2.BotSession.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='google.devtools.remoteworkers.v1test2.BotSession.bot_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.devtools.remoteworkers.v1test2.BotSession.status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='worker', full_name='google.devtools.remoteworkers.v1test2.BotSession.worker', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='leases', full_name='google.devtools.remoteworkers.v1test2.BotSession.leases', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expire_time', full_name='google.devtools.remoteworkers.v1test2.BotSession.expire_time', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.devtools.remoteworkers.v1test2.BotSession.version', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=191,
  serialized_end=490,
)


_LEASE = _descriptor.Descriptor(
  name='Lease',
  full_name='google.devtools.remoteworkers.v1test2.Lease',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='assignment', full_name='google.devtools.remoteworkers.v1test2.Lease.assignment', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='state', full_name='google.devtools.remoteworkers.v1test2.Lease.state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.devtools.remoteworkers.v1test2.Lease.status', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requirements', full_name='google.devtools.remoteworkers.v1test2.Lease.requirements', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expire_time', full_name='google.devtools.remoteworkers.v1test2.Lease.expire_time', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inline_assignment', full_name='google.devtools.remoteworkers.v1test2.Lease.inline_assignment', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=493,
  serialized_end=789,
)


_WORKER_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='google.devtools.remoteworkers.v1test2.Worker.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.devtools.remoteworkers.v1test2.Worker.Property.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.devtools.remoteworkers.v1test2.Worker.Property.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=942,
  serialized_end=980,
)

_WORKER = _descriptor.Descriptor(
  name='Worker',
  full_name='google.devtools.remoteworkers.v1test2.Worker',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='google.devtools.remoteworkers.v1test2.Worker.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='properties', full_name='google.devtools.remoteworkers.v1test2.Worker.properties', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_WORKER_PROPERTY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=792,
  serialized_end=980,
)


_DEVICE_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='google.devtools.remoteworkers.v1test2.Device.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.devtools.remoteworkers.v1test2.Device.Property.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.devtools.remoteworkers.v1test2.Device.Property.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=942,
  serialized_end=980,
)

_DEVICE = _descriptor.Descriptor(
  name='Device',
  full_name='google.devtools.remoteworkers.v1test2.Device',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='handle', full_name='google.devtools.remoteworkers.v1test2.Device.handle', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='properties', full_name='google.devtools.remoteworkers.v1test2.Device.properties', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DEVICE_PROPERTY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=983,
  serialized_end=1123,
)


_ADMINTEMP = _descriptor.Descriptor(
  name='AdminTemp',
  full_name='google.devtools.remoteworkers.v1test2.AdminTemp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='google.devtools.remoteworkers.v1test2.AdminTemp.command', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='arg', full_name='google.devtools.remoteworkers.v1test2.AdminTemp.arg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADMINTEMP_COMMAND,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1126,
  serialized_end=1323,
)


_CREATEBOTSESSIONREQUEST = _descriptor.Descriptor(
  name='CreateBotSessionRequest',
  full_name='google.devtools.remoteworkers.v1test2.CreateBotSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent', full_name='google.devtools.remoteworkers.v1test2.CreateBotSessionRequest.parent', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_session', full_name='google.devtools.remoteworkers.v1test2.CreateBotSessionRequest.bot_session', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1325,
  serialized_end=1438,
)


_UPDATEBOTSESSIONREQUEST = _descriptor.Descriptor(
  name='UpdateBotSessionRequest',
  full_name='google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_session', full_name='google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest.bot_session', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest.update_mask', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1441,
  serialized_end=1601,
)


_POSTBOTEVENTTEMPREQUEST = _descriptor.Descriptor(
  name='PostBotEventTempRequest',
  full_name='google.devtools.remoteworkers.v1test2.PostBotEventTempRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.devtools.remoteworkers.v1test2.PostBotEventTempRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.devtools.remoteworkers.v1test2.PostBotEventTempRequest.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='google.devtools.remoteworkers.v1test2.PostBotEventTempRequest.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _POSTBOTEVENTTEMPREQUEST_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1604,
  serialized_end=1785,
)

_BOTSESSION.fields_by_name['status'].enum_type = _BOTSTATUS
_BOTSESSION.fields_by_name['worker'].message_type = _WORKER
_BOTSESSION.fields_by_name['leases'].message_type = _LEASE
_BOTSESSION.fields_by_name['expire_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LEASE.fields_by_name['state'].enum_type = _LEASESTATE
_LEASE.fields_by_name['status'].message_type = status__pb2._STATUS
_LEASE.fields_by_name['requirements'].message_type = _WORKER
_LEASE.fields_by_name['expire_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LEASE.fields_by_name['inline_assignment'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_WORKER_PROPERTY.containing_type = _WORKER
_WORKER.fields_by_name['devices'].message_type = _DEVICE
_WORKER.fields_by_name['properties'].message_type = _WORKER_PROPERTY
_DEVICE_PROPERTY.containing_type = _DEVICE
_DEVICE.fields_by_name['properties'].message_type = _DEVICE_PROPERTY
_ADMINTEMP.fields_by_name['command'].enum_type = _ADMINTEMP_COMMAND
_ADMINTEMP_COMMAND.containing_type = _ADMINTEMP
_CREATEBOTSESSIONREQUEST.fields_by_name['bot_session'].message_type = _BOTSESSION
_UPDATEBOTSESSIONREQUEST.fields_by_name['bot_session'].message_type = _BOTSESSION
_UPDATEBOTSESSIONREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_POSTBOTEVENTTEMPREQUEST.fields_by_name['type'].enum_type = _POSTBOTEVENTTEMPREQUEST_TYPE
_POSTBOTEVENTTEMPREQUEST_TYPE.containing_type = _POSTBOTEVENTTEMPREQUEST
DESCRIPTOR.message_types_by_name['BotSession'] = _BOTSESSION
DESCRIPTOR.message_types_by_name['Lease'] = _LEASE
DESCRIPTOR.message_types_by_name['Worker'] = _WORKER
DESCRIPTOR.message_types_by_name['Device'] = _DEVICE
DESCRIPTOR.message_types_by_name['AdminTemp'] = _ADMINTEMP
DESCRIPTOR.message_types_by_name['CreateBotSessionRequest'] = _CREATEBOTSESSIONREQUEST
DESCRIPTOR.message_types_by_name['UpdateBotSessionRequest'] = _UPDATEBOTSESSIONREQUEST
DESCRIPTOR.message_types_by_name['PostBotEventTempRequest'] = _POSTBOTEVENTTEMPREQUEST
DESCRIPTOR.enum_types_by_name['BotStatus'] = _BOTSTATUS
DESCRIPTOR.enum_types_by_name['LeaseState'] = _LEASESTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BotSession = _reflection.GeneratedProtocolMessageType('BotSession', (_message.Message,), dict(
  DESCRIPTOR = _BOTSESSION,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.BotSession)
  ))
_sym_db.RegisterMessage(BotSession)

Lease = _reflection.GeneratedProtocolMessageType('Lease', (_message.Message,), dict(
  DESCRIPTOR = _LEASE,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.Lease)
  ))
_sym_db.RegisterMessage(Lease)

Worker = _reflection.GeneratedProtocolMessageType('Worker', (_message.Message,), dict(

  Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), dict(
    DESCRIPTOR = _WORKER_PROPERTY,
    __module__ = 'bots_pb2'
    # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.Worker.Property)
    ))
  ,
  DESCRIPTOR = _WORKER,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.Worker)
  ))
_sym_db.RegisterMessage(Worker)
_sym_db.RegisterMessage(Worker.Property)

Device = _reflection.GeneratedProtocolMessageType('Device', (_message.Message,), dict(

  Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), dict(
    DESCRIPTOR = _DEVICE_PROPERTY,
    __module__ = 'bots_pb2'
    # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.Device.Property)
    ))
  ,
  DESCRIPTOR = _DEVICE,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.Device)
  ))
_sym_db.RegisterMessage(Device)
_sym_db.RegisterMessage(Device.Property)

AdminTemp = _reflection.GeneratedProtocolMessageType('AdminTemp', (_message.Message,), dict(
  DESCRIPTOR = _ADMINTEMP,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.AdminTemp)
  ))
_sym_db.RegisterMessage(AdminTemp)

CreateBotSessionRequest = _reflection.GeneratedProtocolMessageType('CreateBotSessionRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEBOTSESSIONREQUEST,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.CreateBotSessionRequest)
  ))
_sym_db.RegisterMessage(CreateBotSessionRequest)

UpdateBotSessionRequest = _reflection.GeneratedProtocolMessageType('UpdateBotSessionRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEBOTSESSIONREQUEST,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.UpdateBotSessionRequest)
  ))
_sym_db.RegisterMessage(UpdateBotSessionRequest)

PostBotEventTempRequest = _reflection.GeneratedProtocolMessageType('PostBotEventTempRequest', (_message.Message,), dict(
  DESCRIPTOR = _POSTBOTEVENTTEMPREQUEST,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:google.devtools.remoteworkers.v1test2.PostBotEventTempRequest)
  ))
_sym_db.RegisterMessage(PostBotEventTempRequest)



_BOTS = _descriptor.ServiceDescriptor(
  name='Bots',
  full_name='google.devtools.remoteworkers.v1test2.Bots',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=1991,
  serialized_end=2377,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateBotSession',
    full_name='google.devtools.remoteworkers.v1test2.Bots.CreateBotSession',
    index=0,
    containing_service=None,
    input_type=_CREATEBOTSESSIONREQUEST,
    output_type=_BOTSESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateBotSession',
    full_name='google.devtools.remoteworkers.v1test2.Bots.UpdateBotSession',
    index=1,
    containing_service=None,
    input_type=_UPDATEBOTSESSIONREQUEST,
    output_type=_BOTSESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PostBotEventTemp',
    full_name='google.devtools.remoteworkers.v1test2.Bots.PostBotEventTemp',
    index=2,
    containing_service=None,
    input_type=_POSTBOTEVENTTEMPREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_BOTS)

DESCRIPTOR.services_by_name['Bots'] = _BOTS

# @@protoc_insertion_point(module_scope)
