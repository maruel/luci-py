# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: config.proto

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
  name='config.proto',
  package='gce_backend',
  syntax='proto2',
  serialized_pb=_b('\n\x0c\x63onfig.proto\x12\x0bgce_backend\"\xa0\x04\n\x16InstanceTemplateConfig\x12G\n\ttemplates\x18\x01 \x03(\x0b\x32\x34.gce_backend.InstanceTemplateConfig.InstanceTemplate\x1a\xbc\x03\n\x10InstanceTemplate\x12\x11\n\tbase_name\x18\x01 \x01(\t\x12\x0f\n\x07project\x18\x02 \x01(\t\x12\x12\n\ndimensions\x18\x03 \x03(\t\x12\x12\n\nimage_name\x18\x04 \x01(\t\x12\x15\n\rimage_project\x18\n \x01(\t\x12\x14\n\x0c\x64isk_size_gb\x18\x05 \x01(\x05\x12]\n\x10service_accounts\x18\x06 \x03(\x0b\x32\x43.gce_backend.InstanceTemplateConfig.InstanceTemplate.ServiceAccount\x12\x0c\n\x04tags\x18\x07 \x03(\t\x12\x10\n\x08metadata\x18\x08 \x03(\t\x12\x14\n\x0cmachine_type\x18\t \x01(\t\x12\x13\n\x0bnetwork_url\x18\x0b \x01(\t\x12\x1f\n\x17\x61uto_assign_external_ip\x18\x0c \x01(\x08\x12\x18\n\x10min_cpu_platform\x18\r \x01(\t\x12\x1a\n\x12metadata_from_file\x18\x0e \x03(\t\x1a.\n\x0eServiceAccount\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06scopes\x18\x02 \x03(\t\"\xda\x01\n\x1aInstanceGroupManagerConfig\x12N\n\x08managers\x18\x01 \x03(\x0b\x32<.gce_backend.InstanceGroupManagerConfig.InstanceGroupManager\x1al\n\x14InstanceGroupManager\x12\x1a\n\x12template_base_name\x18\x01 \x01(\t\x12\x14\n\x0cminimum_size\x18\x02 \x01(\x05\x12\x14\n\x0cmaximum_size\x18\x03 \x01(\x05\x12\x0c\n\x04zone\x18\x04 \x01(\t\">\n\x0bSettingsCfg\x12\x1c\n\x14\x65nable_ts_monitoring\x18\x01 \x01(\x08\x12\x11\n\tmp_server\x18\x02 \x01(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE_SERVICEACCOUNT = _descriptor.Descriptor(
  name='ServiceAccount',
  full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.ServiceAccount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.ServiceAccount.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scopes', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.ServiceAccount.scopes', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=528,
  serialized_end=574,
)

_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE = _descriptor.Descriptor(
  name='InstanceTemplate',
  full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_name', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.base_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='project', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.project', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.dimensions', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_name', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.image_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_project', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.image_project', index=4,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='disk_size_gb', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.disk_size_gb', index=5,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_accounts', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.service_accounts', index=6,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tags', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.tags', index=7,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.metadata', index=8,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='machine_type', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.machine_type', index=9,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='network_url', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.network_url', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auto_assign_external_ip', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.auto_assign_external_ip', index=11,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_cpu_platform', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.min_cpu_platform', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='metadata_from_file', full_name='gce_backend.InstanceTemplateConfig.InstanceTemplate.metadata_from_file', index=13,
      number=14, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE_SERVICEACCOUNT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=574,
)

_INSTANCETEMPLATECONFIG = _descriptor.Descriptor(
  name='InstanceTemplateConfig',
  full_name='gce_backend.InstanceTemplateConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='templates', full_name='gce_backend.InstanceTemplateConfig.templates', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=574,
)


_INSTANCEGROUPMANAGERCONFIG_INSTANCEGROUPMANAGER = _descriptor.Descriptor(
  name='InstanceGroupManager',
  full_name='gce_backend.InstanceGroupManagerConfig.InstanceGroupManager',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='template_base_name', full_name='gce_backend.InstanceGroupManagerConfig.InstanceGroupManager.template_base_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='minimum_size', full_name='gce_backend.InstanceGroupManagerConfig.InstanceGroupManager.minimum_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maximum_size', full_name='gce_backend.InstanceGroupManagerConfig.InstanceGroupManager.maximum_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zone', full_name='gce_backend.InstanceGroupManagerConfig.InstanceGroupManager.zone', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=687,
  serialized_end=795,
)

_INSTANCEGROUPMANAGERCONFIG = _descriptor.Descriptor(
  name='InstanceGroupManagerConfig',
  full_name='gce_backend.InstanceGroupManagerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='managers', full_name='gce_backend.InstanceGroupManagerConfig.managers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_INSTANCEGROUPMANAGERCONFIG_INSTANCEGROUPMANAGER, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=577,
  serialized_end=795,
)


_SETTINGSCFG = _descriptor.Descriptor(
  name='SettingsCfg',
  full_name='gce_backend.SettingsCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enable_ts_monitoring', full_name='gce_backend.SettingsCfg.enable_ts_monitoring', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mp_server', full_name='gce_backend.SettingsCfg.mp_server', index=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=797,
  serialized_end=859,
)

_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE_SERVICEACCOUNT.containing_type = _INSTANCETEMPLATECONFIG_INSTANCETEMPLATE
_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE.fields_by_name['service_accounts'].message_type = _INSTANCETEMPLATECONFIG_INSTANCETEMPLATE_SERVICEACCOUNT
_INSTANCETEMPLATECONFIG_INSTANCETEMPLATE.containing_type = _INSTANCETEMPLATECONFIG
_INSTANCETEMPLATECONFIG.fields_by_name['templates'].message_type = _INSTANCETEMPLATECONFIG_INSTANCETEMPLATE
_INSTANCEGROUPMANAGERCONFIG_INSTANCEGROUPMANAGER.containing_type = _INSTANCEGROUPMANAGERCONFIG
_INSTANCEGROUPMANAGERCONFIG.fields_by_name['managers'].message_type = _INSTANCEGROUPMANAGERCONFIG_INSTANCEGROUPMANAGER
DESCRIPTOR.message_types_by_name['InstanceTemplateConfig'] = _INSTANCETEMPLATECONFIG
DESCRIPTOR.message_types_by_name['InstanceGroupManagerConfig'] = _INSTANCEGROUPMANAGERCONFIG
DESCRIPTOR.message_types_by_name['SettingsCfg'] = _SETTINGSCFG

InstanceTemplateConfig = _reflection.GeneratedProtocolMessageType('InstanceTemplateConfig', (_message.Message,), dict(

  InstanceTemplate = _reflection.GeneratedProtocolMessageType('InstanceTemplate', (_message.Message,), dict(

    ServiceAccount = _reflection.GeneratedProtocolMessageType('ServiceAccount', (_message.Message,), dict(
      DESCRIPTOR = _INSTANCETEMPLATECONFIG_INSTANCETEMPLATE_SERVICEACCOUNT,
      __module__ = 'config_pb2'
      # @@protoc_insertion_point(class_scope:gce_backend.InstanceTemplateConfig.InstanceTemplate.ServiceAccount)
      ))
    ,
    DESCRIPTOR = _INSTANCETEMPLATECONFIG_INSTANCETEMPLATE,
    __module__ = 'config_pb2'
    # @@protoc_insertion_point(class_scope:gce_backend.InstanceTemplateConfig.InstanceTemplate)
    ))
  ,
  DESCRIPTOR = _INSTANCETEMPLATECONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:gce_backend.InstanceTemplateConfig)
  ))
_sym_db.RegisterMessage(InstanceTemplateConfig)
_sym_db.RegisterMessage(InstanceTemplateConfig.InstanceTemplate)
_sym_db.RegisterMessage(InstanceTemplateConfig.InstanceTemplate.ServiceAccount)

InstanceGroupManagerConfig = _reflection.GeneratedProtocolMessageType('InstanceGroupManagerConfig', (_message.Message,), dict(

  InstanceGroupManager = _reflection.GeneratedProtocolMessageType('InstanceGroupManager', (_message.Message,), dict(
    DESCRIPTOR = _INSTANCEGROUPMANAGERCONFIG_INSTANCEGROUPMANAGER,
    __module__ = 'config_pb2'
    # @@protoc_insertion_point(class_scope:gce_backend.InstanceGroupManagerConfig.InstanceGroupManager)
    ))
  ,
  DESCRIPTOR = _INSTANCEGROUPMANAGERCONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:gce_backend.InstanceGroupManagerConfig)
  ))
_sym_db.RegisterMessage(InstanceGroupManagerConfig)
_sym_db.RegisterMessage(InstanceGroupManagerConfig.InstanceGroupManager)

SettingsCfg = _reflection.GeneratedProtocolMessageType('SettingsCfg', (_message.Message,), dict(
  DESCRIPTOR = _SETTINGSCFG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:gce_backend.SettingsCfg)
  ))
_sym_db.RegisterMessage(SettingsCfg)


# @@protoc_insertion_point(module_scope)
