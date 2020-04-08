# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: components/config/proto/service_config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='components/config/proto/service_config.proto',
  package='config',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n,components/config/proto/service_config.proto\x12\x06\x63onfig\"\x84\x01\n\x11\x43onfigSetLocation\x12\x0b\n\x03url\x18\x01 \x01(\t\x12;\n\x0cstorage_type\x18\x02 \x01(\x0e\x32%.config.ConfigSetLocation.StorageType\"%\n\x0bStorageType\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07GITILES\x10\x01\"/\n\x0eIdentityConfig\x12\x1d\n\x15service_account_email\x18\x01 \x01(\t\"z\n\x07Project\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x0f\x63onfig_location\x18\x02 \x01(\x0b\x32\x19.config.ConfigSetLocation\x12/\n\x0fidentity_config\x18\x03 \x01(\x0b\x32\x16.config.IdentityConfig\"0\n\x0bProjectsCfg\x12!\n\x08projects\x18\x01 \x03(\x0b\x32\x0f.config.Project\"\xc7\x01\n\x07Service\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06owners\x18\x02 \x03(\t\x12\x32\n\x0f\x63onfig_location\x18\x03 \x01(\x0b\x32\x19.config.ConfigSetLocation\x12\x14\n\x0cmetadata_url\x18\x04 \x01(\t\x12\x0e\n\x06\x61\x63\x63\x65ss\x18\x05 \x03(\t\x12)\n\x08jwt_auth\x18\x06 \x01(\x0b\x32\x17.config.Service.JWTAuth\x1a\x1b\n\x07JWTAuth\x12\x10\n\x08\x61udience\x18\x01 \x01(\t\"P\n\x16ServiceDynamicMetadata\x12\x0f\n\x07version\x18\x01 \x01(\t\x12%\n\nvalidation\x18\x02 \x01(\x0b\x32\x11.config.Validator\"0\n\x0bServicesCfg\x12!\n\x08services\x18\x01 \x03(\x0b\x32\x0f.config.Service\"\xab\x01\n\x06\x41\x63lCfg\x12\x1c\n\x14project_access_group\x18\x02 \x01(\t\x12\x1c\n\x14service_access_group\x18\x07 \x01(\t\x12\x13\n\x0b\x61\x64min_group\x18\x03 \x01(\t\x12\x18\n\x10validation_group\x18\x05 \x01(\t\x12\x16\n\x0ereimport_group\x18\x06 \x01(\tJ\x04\x08\x04\x10\x05R\x18\x63onfig_get_by_hash_group\"\xe9\x01\n\tImportCfg\x12*\n\x07gitiles\x18\x01 \x01(\x0b\x32\x19.config.ImportCfg.Gitiles\x1a\xaf\x01\n\x07Gitiles\x12\x1a\n\x12\x66\x65tch_log_deadline\x18\x01 \x01(\x05\x12\x1e\n\x16\x66\x65tch_archive_deadline\x18\x02 \x01(\x05\x12\"\n\x1aproject_config_default_ref\x18\x03 \x01(\t\x12#\n\x1bproject_config_default_path\x18\x04 \x01(\t\x12\x1f\n\x17ref_config_default_path\x18\x05 \x01(\t\"]\n\nSchemasCfg\x12*\n\x07schemas\x18\x01 \x03(\x0b\x32\x19.config.SchemasCfg.Schema\x1a#\n\x06Schema\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\"1\n\rConfigPattern\x12\x12\n\nconfig_set\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"A\n\tValidator\x12\'\n\x08patterns\x18\x01 \x03(\x0b\x32\x15.config.ConfigPattern\x12\x0b\n\x03url\x18\x02 \x01(\t\"M\n\x18ValidationRequestMessage\x12\x12\n\nconfig_set\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\x0c\"\x91\x02\n\x19ValidationResponseMessage\x12;\n\x08messages\x18\x01 \x03(\x0b\x32).config.ValidationResponseMessage.Message\x1a\x63\n\x07Message\x12\x0c\n\x04path\x18\x01 \x01(\t\x12<\n\x08severity\x18\x02 \x01(\x0e\x32*.config.ValidationResponseMessage.Severity\x12\x0c\n\x04text\x18\x03 \x01(\t\"R\n\x08Severity\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05\x44\x45\x42UG\x10\n\x12\x08\n\x04INFO\x10\x14\x12\x0b\n\x07WARNING\x10\x1e\x12\t\n\x05\x45RROR\x10(\x12\x0c\n\x08\x43RITICAL\x10\x32\x62\x06proto3')
)



_CONFIGSETLOCATION_STORAGETYPE = _descriptor.EnumDescriptor(
  name='StorageType',
  full_name='config.ConfigSetLocation.StorageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSET', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GITILES', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=152,
  serialized_end=189,
)
_sym_db.RegisterEnumDescriptor(_CONFIGSETLOCATION_STORAGETYPE)

_VALIDATIONRESPONSEMESSAGE_SEVERITY = _descriptor.EnumDescriptor(
  name='Severity',
  full_name='config.ValidationResponseMessage.Severity',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEBUG', index=1, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO', index=2, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WARNING', index=3, number=30,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=4, number=40,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRITICAL', index=5, number=50,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1642,
  serialized_end=1724,
)
_sym_db.RegisterEnumDescriptor(_VALIDATIONRESPONSEMESSAGE_SEVERITY)


_CONFIGSETLOCATION = _descriptor.Descriptor(
  name='ConfigSetLocation',
  full_name='config.ConfigSetLocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='config.ConfigSetLocation.url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='storage_type', full_name='config.ConfigSetLocation.storage_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONFIGSETLOCATION_STORAGETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=189,
)


_IDENTITYCONFIG = _descriptor.Descriptor(
  name='IdentityConfig',
  full_name='config.IdentityConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='service_account_email', full_name='config.IdentityConfig.service_account_email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=191,
  serialized_end=238,
)


_PROJECT = _descriptor.Descriptor(
  name='Project',
  full_name='config.Project',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='config.Project.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config_location', full_name='config.Project.config_location', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='identity_config', full_name='config.Project.identity_config', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=240,
  serialized_end=362,
)


_PROJECTSCFG = _descriptor.Descriptor(
  name='ProjectsCfg',
  full_name='config.ProjectsCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projects', full_name='config.ProjectsCfg.projects', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=364,
  serialized_end=412,
)


_SERVICE_JWTAUTH = _descriptor.Descriptor(
  name='JWTAuth',
  full_name='config.Service.JWTAuth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='audience', full_name='config.Service.JWTAuth.audience', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=587,
  serialized_end=614,
)

_SERVICE = _descriptor.Descriptor(
  name='Service',
  full_name='config.Service',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='config.Service.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owners', full_name='config.Service.owners', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config_location', full_name='config.Service.config_location', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata_url', full_name='config.Service.metadata_url', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='access', full_name='config.Service.access', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='jwt_auth', full_name='config.Service.jwt_auth', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SERVICE_JWTAUTH, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=415,
  serialized_end=614,
)


_SERVICEDYNAMICMETADATA = _descriptor.Descriptor(
  name='ServiceDynamicMetadata',
  full_name='config.ServiceDynamicMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='config.ServiceDynamicMetadata.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validation', full_name='config.ServiceDynamicMetadata.validation', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=616,
  serialized_end=696,
)


_SERVICESCFG = _descriptor.Descriptor(
  name='ServicesCfg',
  full_name='config.ServicesCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='services', full_name='config.ServicesCfg.services', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=698,
  serialized_end=746,
)


_ACLCFG = _descriptor.Descriptor(
  name='AclCfg',
  full_name='config.AclCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='project_access_group', full_name='config.AclCfg.project_access_group', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='service_access_group', full_name='config.AclCfg.service_access_group', index=1,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='admin_group', full_name='config.AclCfg.admin_group', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validation_group', full_name='config.AclCfg.validation_group', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reimport_group', full_name='config.AclCfg.reimport_group', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=749,
  serialized_end=920,
)


_IMPORTCFG_GITILES = _descriptor.Descriptor(
  name='Gitiles',
  full_name='config.ImportCfg.Gitiles',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fetch_log_deadline', full_name='config.ImportCfg.Gitiles.fetch_log_deadline', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fetch_archive_deadline', full_name='config.ImportCfg.Gitiles.fetch_archive_deadline', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='project_config_default_ref', full_name='config.ImportCfg.Gitiles.project_config_default_ref', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='project_config_default_path', full_name='config.ImportCfg.Gitiles.project_config_default_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ref_config_default_path', full_name='config.ImportCfg.Gitiles.ref_config_default_path', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=981,
  serialized_end=1156,
)

_IMPORTCFG = _descriptor.Descriptor(
  name='ImportCfg',
  full_name='config.ImportCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gitiles', full_name='config.ImportCfg.gitiles', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_IMPORTCFG_GITILES, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=923,
  serialized_end=1156,
)


_SCHEMASCFG_SCHEMA = _descriptor.Descriptor(
  name='Schema',
  full_name='config.SchemasCfg.Schema',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='config.SchemasCfg.Schema.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url', full_name='config.SchemasCfg.Schema.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1216,
  serialized_end=1251,
)

_SCHEMASCFG = _descriptor.Descriptor(
  name='SchemasCfg',
  full_name='config.SchemasCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='schemas', full_name='config.SchemasCfg.schemas', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SCHEMASCFG_SCHEMA, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1158,
  serialized_end=1251,
)


_CONFIGPATTERN = _descriptor.Descriptor(
  name='ConfigPattern',
  full_name='config.ConfigPattern',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config_set', full_name='config.ConfigPattern.config_set', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='config.ConfigPattern.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1253,
  serialized_end=1302,
)


_VALIDATOR = _descriptor.Descriptor(
  name='Validator',
  full_name='config.Validator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='patterns', full_name='config.Validator.patterns', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url', full_name='config.Validator.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1304,
  serialized_end=1369,
)


_VALIDATIONREQUESTMESSAGE = _descriptor.Descriptor(
  name='ValidationRequestMessage',
  full_name='config.ValidationRequestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config_set', full_name='config.ValidationRequestMessage.config_set', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='config.ValidationRequestMessage.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='config.ValidationRequestMessage.content', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1371,
  serialized_end=1448,
)


_VALIDATIONRESPONSEMESSAGE_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='config.ValidationResponseMessage.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='config.ValidationResponseMessage.Message.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='config.ValidationResponseMessage.Message.severity', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='config.ValidationResponseMessage.Message.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1541,
  serialized_end=1640,
)

_VALIDATIONRESPONSEMESSAGE = _descriptor.Descriptor(
  name='ValidationResponseMessage',
  full_name='config.ValidationResponseMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='messages', full_name='config.ValidationResponseMessage.messages', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_VALIDATIONRESPONSEMESSAGE_MESSAGE, ],
  enum_types=[
    _VALIDATIONRESPONSEMESSAGE_SEVERITY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1451,
  serialized_end=1724,
)

_CONFIGSETLOCATION.fields_by_name['storage_type'].enum_type = _CONFIGSETLOCATION_STORAGETYPE
_CONFIGSETLOCATION_STORAGETYPE.containing_type = _CONFIGSETLOCATION
_PROJECT.fields_by_name['config_location'].message_type = _CONFIGSETLOCATION
_PROJECT.fields_by_name['identity_config'].message_type = _IDENTITYCONFIG
_PROJECTSCFG.fields_by_name['projects'].message_type = _PROJECT
_SERVICE_JWTAUTH.containing_type = _SERVICE
_SERVICE.fields_by_name['config_location'].message_type = _CONFIGSETLOCATION
_SERVICE.fields_by_name['jwt_auth'].message_type = _SERVICE_JWTAUTH
_SERVICEDYNAMICMETADATA.fields_by_name['validation'].message_type = _VALIDATOR
_SERVICESCFG.fields_by_name['services'].message_type = _SERVICE
_IMPORTCFG_GITILES.containing_type = _IMPORTCFG
_IMPORTCFG.fields_by_name['gitiles'].message_type = _IMPORTCFG_GITILES
_SCHEMASCFG_SCHEMA.containing_type = _SCHEMASCFG
_SCHEMASCFG.fields_by_name['schemas'].message_type = _SCHEMASCFG_SCHEMA
_VALIDATOR.fields_by_name['patterns'].message_type = _CONFIGPATTERN
_VALIDATIONRESPONSEMESSAGE_MESSAGE.fields_by_name['severity'].enum_type = _VALIDATIONRESPONSEMESSAGE_SEVERITY
_VALIDATIONRESPONSEMESSAGE_MESSAGE.containing_type = _VALIDATIONRESPONSEMESSAGE
_VALIDATIONRESPONSEMESSAGE.fields_by_name['messages'].message_type = _VALIDATIONRESPONSEMESSAGE_MESSAGE
_VALIDATIONRESPONSEMESSAGE_SEVERITY.containing_type = _VALIDATIONRESPONSEMESSAGE
DESCRIPTOR.message_types_by_name['ConfigSetLocation'] = _CONFIGSETLOCATION
DESCRIPTOR.message_types_by_name['IdentityConfig'] = _IDENTITYCONFIG
DESCRIPTOR.message_types_by_name['Project'] = _PROJECT
DESCRIPTOR.message_types_by_name['ProjectsCfg'] = _PROJECTSCFG
DESCRIPTOR.message_types_by_name['Service'] = _SERVICE
DESCRIPTOR.message_types_by_name['ServiceDynamicMetadata'] = _SERVICEDYNAMICMETADATA
DESCRIPTOR.message_types_by_name['ServicesCfg'] = _SERVICESCFG
DESCRIPTOR.message_types_by_name['AclCfg'] = _ACLCFG
DESCRIPTOR.message_types_by_name['ImportCfg'] = _IMPORTCFG
DESCRIPTOR.message_types_by_name['SchemasCfg'] = _SCHEMASCFG
DESCRIPTOR.message_types_by_name['ConfigPattern'] = _CONFIGPATTERN
DESCRIPTOR.message_types_by_name['Validator'] = _VALIDATOR
DESCRIPTOR.message_types_by_name['ValidationRequestMessage'] = _VALIDATIONREQUESTMESSAGE
DESCRIPTOR.message_types_by_name['ValidationResponseMessage'] = _VALIDATIONRESPONSEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConfigSetLocation = _reflection.GeneratedProtocolMessageType('ConfigSetLocation', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGSETLOCATION,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ConfigSetLocation)
  ))
_sym_db.RegisterMessage(ConfigSetLocation)

IdentityConfig = _reflection.GeneratedProtocolMessageType('IdentityConfig', (_message.Message,), dict(
  DESCRIPTOR = _IDENTITYCONFIG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.IdentityConfig)
  ))
_sym_db.RegisterMessage(IdentityConfig)

Project = _reflection.GeneratedProtocolMessageType('Project', (_message.Message,), dict(
  DESCRIPTOR = _PROJECT,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.Project)
  ))
_sym_db.RegisterMessage(Project)

ProjectsCfg = _reflection.GeneratedProtocolMessageType('ProjectsCfg', (_message.Message,), dict(
  DESCRIPTOR = _PROJECTSCFG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ProjectsCfg)
  ))
_sym_db.RegisterMessage(ProjectsCfg)

Service = _reflection.GeneratedProtocolMessageType('Service', (_message.Message,), dict(

  JWTAuth = _reflection.GeneratedProtocolMessageType('JWTAuth', (_message.Message,), dict(
    DESCRIPTOR = _SERVICE_JWTAUTH,
    __module__ = 'components.config.proto.service_config_pb2'
    # @@protoc_insertion_point(class_scope:config.Service.JWTAuth)
    ))
  ,
  DESCRIPTOR = _SERVICE,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.Service)
  ))
_sym_db.RegisterMessage(Service)
_sym_db.RegisterMessage(Service.JWTAuth)

ServiceDynamicMetadata = _reflection.GeneratedProtocolMessageType('ServiceDynamicMetadata', (_message.Message,), dict(
  DESCRIPTOR = _SERVICEDYNAMICMETADATA,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ServiceDynamicMetadata)
  ))
_sym_db.RegisterMessage(ServiceDynamicMetadata)

ServicesCfg = _reflection.GeneratedProtocolMessageType('ServicesCfg', (_message.Message,), dict(
  DESCRIPTOR = _SERVICESCFG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ServicesCfg)
  ))
_sym_db.RegisterMessage(ServicesCfg)

AclCfg = _reflection.GeneratedProtocolMessageType('AclCfg', (_message.Message,), dict(
  DESCRIPTOR = _ACLCFG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.AclCfg)
  ))
_sym_db.RegisterMessage(AclCfg)

ImportCfg = _reflection.GeneratedProtocolMessageType('ImportCfg', (_message.Message,), dict(

  Gitiles = _reflection.GeneratedProtocolMessageType('Gitiles', (_message.Message,), dict(
    DESCRIPTOR = _IMPORTCFG_GITILES,
    __module__ = 'components.config.proto.service_config_pb2'
    # @@protoc_insertion_point(class_scope:config.ImportCfg.Gitiles)
    ))
  ,
  DESCRIPTOR = _IMPORTCFG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ImportCfg)
  ))
_sym_db.RegisterMessage(ImportCfg)
_sym_db.RegisterMessage(ImportCfg.Gitiles)

SchemasCfg = _reflection.GeneratedProtocolMessageType('SchemasCfg', (_message.Message,), dict(

  Schema = _reflection.GeneratedProtocolMessageType('Schema', (_message.Message,), dict(
    DESCRIPTOR = _SCHEMASCFG_SCHEMA,
    __module__ = 'components.config.proto.service_config_pb2'
    # @@protoc_insertion_point(class_scope:config.SchemasCfg.Schema)
    ))
  ,
  DESCRIPTOR = _SCHEMASCFG,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.SchemasCfg)
  ))
_sym_db.RegisterMessage(SchemasCfg)
_sym_db.RegisterMessage(SchemasCfg.Schema)

ConfigPattern = _reflection.GeneratedProtocolMessageType('ConfigPattern', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGPATTERN,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ConfigPattern)
  ))
_sym_db.RegisterMessage(ConfigPattern)

Validator = _reflection.GeneratedProtocolMessageType('Validator', (_message.Message,), dict(
  DESCRIPTOR = _VALIDATOR,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.Validator)
  ))
_sym_db.RegisterMessage(Validator)

ValidationRequestMessage = _reflection.GeneratedProtocolMessageType('ValidationRequestMessage', (_message.Message,), dict(
  DESCRIPTOR = _VALIDATIONREQUESTMESSAGE,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ValidationRequestMessage)
  ))
_sym_db.RegisterMessage(ValidationRequestMessage)

ValidationResponseMessage = _reflection.GeneratedProtocolMessageType('ValidationResponseMessage', (_message.Message,), dict(

  Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
    DESCRIPTOR = _VALIDATIONRESPONSEMESSAGE_MESSAGE,
    __module__ = 'components.config.proto.service_config_pb2'
    # @@protoc_insertion_point(class_scope:config.ValidationResponseMessage.Message)
    ))
  ,
  DESCRIPTOR = _VALIDATIONRESPONSEMESSAGE,
  __module__ = 'components.config.proto.service_config_pb2'
  # @@protoc_insertion_point(class_scope:config.ValidationResponseMessage)
  ))
_sym_db.RegisterMessage(ValidationResponseMessage)
_sym_db.RegisterMessage(ValidationResponseMessage.Message)


# @@protoc_insertion_point(module_scope)
