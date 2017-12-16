# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bots.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bots.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\nbots.proto\"C\n\x07\x42otsCfg\x12\x1a\n\x12trusted_dimensions\x18\x01 \x03(\t\x12\x1c\n\tbot_group\x18\x02 \x03(\x0b\x32\t.BotGroup\"Z\n\rDailySchedule\x12\r\n\x05start\x18\x01 \x01(\t\x12\x0b\n\x03\x65nd\x18\x02 \x01(\t\x12\x18\n\x10\x64\x61ys_of_the_week\x18\x03 \x03(\x05\x12\x13\n\x0btarget_size\x18\x04 \x01(\x05\"7\n\tLoadBased\x12\x14\n\x0cminimum_size\x18\x01 \x01(\x05\x12\x14\n\x0cmaximum_size\x18\x02 \x01(\x05\"I\n\x08Schedule\x12\x1d\n\x05\x64\x61ily\x18\x01 \x03(\x0b\x32\x0e.DailySchedule\x12\x1e\n\nload_based\x18\x02 \x03(\x0b\x32\n.LoadBased\"\xb2\x01\n\x0bMachineType\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x1a\n\x12\x65\x61rly_release_secs\x18\x03 \x01(\x05\x12\x1b\n\x13lease_duration_secs\x18\x04 \x01(\x05\x12\x15\n\rmp_dimensions\x18\x05 \x03(\t\x12\x13\n\x0btarget_size\x18\x06 \x01(\x05\x12\x1b\n\x08schedule\x18\x07 \x01(\x0b\x32\t.Schedule\"\\\n\x0e\x42otAnnotations\x12\x0e\n\x06\x62ot_id\x18\x01 \x03(\t\x12\x15\n\rbot_id_prefix\x18\x02 \x03(\t\x12\x0f\n\x07mp_name\x18\x03 \x03(\t\x12\x12\n\ndimensions\x18\x04 \x03(\t\"\x97\x02\n\x08\x42otGroup\x12\x0e\n\x06\x62ot_id\x18\x01 \x03(\t\x12\x15\n\rbot_id_prefix\x18\x02 \x03(\t\x12\"\n\x0cmachine_type\x18\x03 \x03(\x0b\x32\x0c.MachineType\x12\x16\n\x04\x61uth\x18\x14 \x01(\x0b\x32\x08.BotAuth\x12\x0e\n\x06owners\x18\x15 \x03(\t\x12\x12\n\ndimensions\x18\x16 \x03(\t\x12\x19\n\x11\x62ot_config_script\x18\x17 \x01(\t\x12\x1e\n\x16system_service_account\x18\x18 \x01(\t\x12(\n\x0f\x62ot_annotations\x18\x19 \x03(\x0b\x32\x0f.BotAnnotations\x12\x1f\n\x17include_bot_annotations\x18\x1a \x01(\t\"d\n\x07\x42otAuth\x12\"\n\x1arequire_luci_machine_token\x18\x01 \x01(\x08\x12\x1f\n\x17require_service_account\x18\x02 \x03(\t\x12\x14\n\x0cip_whitelist\x18\x03 \x01(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BOTSCFG = _descriptor.Descriptor(
  name='BotsCfg',
  full_name='BotsCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trusted_dimensions', full_name='BotsCfg.trusted_dimensions', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_group', full_name='BotsCfg.bot_group', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=81,
)


_DAILYSCHEDULE = _descriptor.Descriptor(
  name='DailySchedule',
  full_name='DailySchedule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='DailySchedule.start', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end', full_name='DailySchedule.end', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='days_of_the_week', full_name='DailySchedule.days_of_the_week', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_size', full_name='DailySchedule.target_size', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=173,
)


_LOADBASED = _descriptor.Descriptor(
  name='LoadBased',
  full_name='LoadBased',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='minimum_size', full_name='LoadBased.minimum_size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maximum_size', full_name='LoadBased.maximum_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=230,
)


_SCHEDULE = _descriptor.Descriptor(
  name='Schedule',
  full_name='Schedule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='daily', full_name='Schedule.daily', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='load_based', full_name='Schedule.load_based', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=232,
  serialized_end=305,
)


_MACHINETYPE = _descriptor.Descriptor(
  name='MachineType',
  full_name='MachineType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='MachineType.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='MachineType.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='early_release_secs', full_name='MachineType.early_release_secs', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lease_duration_secs', full_name='MachineType.lease_duration_secs', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mp_dimensions', full_name='MachineType.mp_dimensions', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_size', full_name='MachineType.target_size', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='schedule', full_name='MachineType.schedule', index=6,
      number=7, type=11, cpp_type=10, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=308,
  serialized_end=486,
)


_BOTANNOTATIONS = _descriptor.Descriptor(
  name='BotAnnotations',
  full_name='BotAnnotations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='BotAnnotations.bot_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_id_prefix', full_name='BotAnnotations.bot_id_prefix', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mp_name', full_name='BotAnnotations.mp_name', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='BotAnnotations.dimensions', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=488,
  serialized_end=580,
)


_BOTGROUP = _descriptor.Descriptor(
  name='BotGroup',
  full_name='BotGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='BotGroup.bot_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_id_prefix', full_name='BotGroup.bot_id_prefix', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='machine_type', full_name='BotGroup.machine_type', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth', full_name='BotGroup.auth', index=3,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='owners', full_name='BotGroup.owners', index=4,
      number=21, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='BotGroup.dimensions', index=5,
      number=22, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_config_script', full_name='BotGroup.bot_config_script', index=6,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='system_service_account', full_name='BotGroup.system_service_account', index=7,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bot_annotations', full_name='BotGroup.bot_annotations', index=8,
      number=25, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='include_bot_annotations', full_name='BotGroup.include_bot_annotations', index=9,
      number=26, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=583,
  serialized_end=862,
)


_BOTAUTH = _descriptor.Descriptor(
  name='BotAuth',
  full_name='BotAuth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='require_luci_machine_token', full_name='BotAuth.require_luci_machine_token', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='require_service_account', full_name='BotAuth.require_service_account', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_whitelist', full_name='BotAuth.ip_whitelist', index=2,
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
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=864,
  serialized_end=964,
)

_BOTSCFG.fields_by_name['bot_group'].message_type = _BOTGROUP
_SCHEDULE.fields_by_name['daily'].message_type = _DAILYSCHEDULE
_SCHEDULE.fields_by_name['load_based'].message_type = _LOADBASED
_MACHINETYPE.fields_by_name['schedule'].message_type = _SCHEDULE
_BOTGROUP.fields_by_name['machine_type'].message_type = _MACHINETYPE
_BOTGROUP.fields_by_name['auth'].message_type = _BOTAUTH
_BOTGROUP.fields_by_name['bot_annotations'].message_type = _BOTANNOTATIONS
DESCRIPTOR.message_types_by_name['BotsCfg'] = _BOTSCFG
DESCRIPTOR.message_types_by_name['DailySchedule'] = _DAILYSCHEDULE
DESCRIPTOR.message_types_by_name['LoadBased'] = _LOADBASED
DESCRIPTOR.message_types_by_name['Schedule'] = _SCHEDULE
DESCRIPTOR.message_types_by_name['MachineType'] = _MACHINETYPE
DESCRIPTOR.message_types_by_name['BotAnnotations'] = _BOTANNOTATIONS
DESCRIPTOR.message_types_by_name['BotGroup'] = _BOTGROUP
DESCRIPTOR.message_types_by_name['BotAuth'] = _BOTAUTH

BotsCfg = _reflection.GeneratedProtocolMessageType('BotsCfg', (_message.Message,), dict(
  DESCRIPTOR = _BOTSCFG,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:BotsCfg)
  ))
_sym_db.RegisterMessage(BotsCfg)

DailySchedule = _reflection.GeneratedProtocolMessageType('DailySchedule', (_message.Message,), dict(
  DESCRIPTOR = _DAILYSCHEDULE,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:DailySchedule)
  ))
_sym_db.RegisterMessage(DailySchedule)

LoadBased = _reflection.GeneratedProtocolMessageType('LoadBased', (_message.Message,), dict(
  DESCRIPTOR = _LOADBASED,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:LoadBased)
  ))
_sym_db.RegisterMessage(LoadBased)

Schedule = _reflection.GeneratedProtocolMessageType('Schedule', (_message.Message,), dict(
  DESCRIPTOR = _SCHEDULE,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:Schedule)
  ))
_sym_db.RegisterMessage(Schedule)

MachineType = _reflection.GeneratedProtocolMessageType('MachineType', (_message.Message,), dict(
  DESCRIPTOR = _MACHINETYPE,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:MachineType)
  ))
_sym_db.RegisterMessage(MachineType)

BotAnnotations = _reflection.GeneratedProtocolMessageType('BotAnnotations', (_message.Message,), dict(
  DESCRIPTOR = _BOTANNOTATIONS,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:BotAnnotations)
  ))
_sym_db.RegisterMessage(BotAnnotations)

BotGroup = _reflection.GeneratedProtocolMessageType('BotGroup', (_message.Message,), dict(
  DESCRIPTOR = _BOTGROUP,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:BotGroup)
  ))
_sym_db.RegisterMessage(BotGroup)

BotAuth = _reflection.GeneratedProtocolMessageType('BotAuth', (_message.Message,), dict(
  DESCRIPTOR = _BOTAUTH,
  __module__ = 'bots_pb2'
  # @@protoc_insertion_point(class_scope:BotAuth)
  ))
_sym_db.RegisterMessage(BotAuth)


# @@protoc_insertion_point(module_scope)
