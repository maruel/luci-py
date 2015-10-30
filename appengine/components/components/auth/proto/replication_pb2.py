# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: replication.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='replication.proto',
  package='components.auth.proto.replication',
  serialized_pb='\n\x11replication.proto\x12!components.auth.proto.replication\"b\n\x11ServiceLinkTicket\x12\x12\n\nprimary_id\x18\x01 \x02(\t\x12\x13\n\x0bprimary_url\x18\x02 \x02(\t\x12\x14\n\x0cgenerated_by\x18\x03 \x02(\t\x12\x0e\n\x06ticket\x18\x04 \x02(\x0c\"O\n\x12ServiceLinkRequest\x12\x0e\n\x06ticket\x18\x01 \x02(\x0c\x12\x13\n\x0breplica_url\x18\x02 \x02(\t\x12\x14\n\x0cinitiated_by\x18\x03 \x02(\t\"\xb0\x01\n\x13ServiceLinkResponse\x12M\n\x06status\x18\x01 \x02(\x0e\x32=.components.auth.proto.replication.ServiceLinkResponse.Status\"J\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\x13\n\x0fTRANSPORT_ERROR\x10\x01\x12\x0e\n\nBAD_TICKET\x10\x02\x12\x0e\n\nAUTH_ERROR\x10\x03\"\xc0\x01\n\tAuthGroup\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0f\n\x07members\x18\x02 \x03(\t\x12\r\n\x05globs\x18\x03 \x03(\t\x12\x0e\n\x06nested\x18\x04 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x02(\t\x12\x12\n\ncreated_ts\x18\x06 \x02(\x03\x12\x12\n\ncreated_by\x18\x07 \x02(\t\x12\x13\n\x0bmodified_ts\x18\x08 \x02(\x03\x12\x13\n\x0bmodified_by\x18\t \x02(\t\x12\x0e\n\x06owners\x18\n \x01(\t\"T\n\nAuthSecret\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06values\x18\x02 \x03(\x0c\x12\x13\n\x0bmodified_ts\x18\x03 \x02(\x03\x12\x13\n\x0bmodified_by\x18\x04 \x02(\t\"\x97\x01\n\x0f\x41uthIPWhitelist\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0f\n\x07subnets\x18\x02 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x02(\t\x12\x12\n\ncreated_ts\x18\x04 \x02(\x03\x12\x12\n\ncreated_by\x18\x05 \x02(\t\x12\x13\n\x0bmodified_ts\x18\x06 \x02(\x03\x12\x13\n\x0bmodified_by\x18\x07 \x02(\t\"|\n\x19\x41uthIPWhitelistAssignment\x12\x10\n\x08identity\x18\x01 \x02(\t\x12\x14\n\x0cip_whitelist\x18\x02 \x02(\t\x12\x0f\n\x07\x63omment\x18\x03 \x02(\t\x12\x12\n\ncreated_ts\x18\x04 \x02(\x03\x12\x12\n\ncreated_by\x18\x05 \x02(\t\"\x8c\x03\n\x06\x41uthDB\x12\x17\n\x0foauth_client_id\x18\x01 \x02(\t\x12\x1b\n\x13oauth_client_secret\x18\x02 \x02(\t\x12#\n\x1boauth_additional_client_ids\x18\x03 \x03(\t\x12<\n\x06groups\x18\x04 \x03(\x0b\x32,.components.auth.proto.replication.AuthGroup\x12>\n\x07secrets\x18\x05 \x03(\x0b\x32-.components.auth.proto.replication.AuthSecret\x12I\n\rip_whitelists\x18\x06 \x03(\x0b\x32\x32.components.auth.proto.replication.AuthIPWhitelist\x12^\n\x18ip_whitelist_assignments\x18\x07 \x03(\x0b\x32<.components.auth.proto.replication.AuthIPWhitelistAssignment\"N\n\x0e\x41uthDBRevision\x12\x12\n\nprimary_id\x18\x01 \x02(\t\x12\x13\n\x0b\x61uth_db_rev\x18\x02 \x02(\x03\x12\x13\n\x0bmodified_ts\x18\x03 \x02(\x03\"Y\n\x12\x43hangeNotification\x12\x43\n\x08revision\x18\x01 \x01(\x0b\x32\x31.components.auth.proto.replication.AuthDBRevision\"\xb4\x01\n\x16ReplicationPushRequest\x12\x43\n\x08revision\x18\x01 \x01(\x0b\x32\x31.components.auth.proto.replication.AuthDBRevision\x12:\n\x07\x61uth_db\x18\x02 \x01(\x0b\x32).components.auth.proto.replication.AuthDB\x12\x19\n\x11\x61uth_code_version\x18\x03 \x01(\t\"\xe2\x03\n\x17ReplicationPushResponse\x12Q\n\x06status\x18\x01 \x02(\x0e\x32\x41.components.auth.proto.replication.ReplicationPushResponse.Status\x12K\n\x10\x63urrent_revision\x18\x02 \x01(\x0b\x32\x31.components.auth.proto.replication.AuthDBRevision\x12X\n\nerror_code\x18\x03 \x01(\x0e\x32\x44.components.auth.proto.replication.ReplicationPushResponse.ErrorCode\x12\x19\n\x11\x61uth_code_version\x18\x04 \x01(\t\"H\n\x06Status\x12\x0b\n\x07\x41PPLIED\x10\x00\x12\x0b\n\x07SKIPPED\x10\x01\x12\x13\n\x0fTRANSIENT_ERROR\x10\x02\x12\x0f\n\x0b\x46\x41TAL_ERROR\x10\x03\"h\n\tErrorCode\x12\x11\n\rNOT_A_REPLICA\x10\x01\x12\r\n\tFORBIDDEN\x10\x02\x12\x15\n\x11MISSING_SIGNATURE\x10\x03\x12\x11\n\rBAD_SIGNATURE\x10\x04\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x05')



_SERVICELINKRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='components.auth.proto.replication.ServiceLinkResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSPORT_ERROR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_TICKET', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AUTH_ERROR', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=340,
  serialized_end=414,
)

_REPLICATIONPUSHRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='components.auth.proto.replication.ReplicationPushResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='APPLIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SKIPPED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSIENT_ERROR', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FATAL_ERROR', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=2035,
  serialized_end=2107,
)

_REPLICATIONPUSHRESPONSE_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='components.auth.proto.replication.ReplicationPushResponse.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NOT_A_REPLICA', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORBIDDEN', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MISSING_SIGNATURE', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_SIGNATURE', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST', index=4, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=2109,
  serialized_end=2213,
)


_SERVICELINKTICKET = _descriptor.Descriptor(
  name='ServiceLinkTicket',
  full_name='components.auth.proto.replication.ServiceLinkTicket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='primary_id', full_name='components.auth.proto.replication.ServiceLinkTicket.primary_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='primary_url', full_name='components.auth.proto.replication.ServiceLinkTicket.primary_url', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='generated_by', full_name='components.auth.proto.replication.ServiceLinkTicket.generated_by', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ticket', full_name='components.auth.proto.replication.ServiceLinkTicket.ticket', index=3,
      number=4, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=56,
  serialized_end=154,
)


_SERVICELINKREQUEST = _descriptor.Descriptor(
  name='ServiceLinkRequest',
  full_name='components.auth.proto.replication.ServiceLinkRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ticket', full_name='components.auth.proto.replication.ServiceLinkRequest.ticket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='replica_url', full_name='components.auth.proto.replication.ServiceLinkRequest.replica_url', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initiated_by', full_name='components.auth.proto.replication.ServiceLinkRequest.initiated_by', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=156,
  serialized_end=235,
)


_SERVICELINKRESPONSE = _descriptor.Descriptor(
  name='ServiceLinkResponse',
  full_name='components.auth.proto.replication.ServiceLinkResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='components.auth.proto.replication.ServiceLinkResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERVICELINKRESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=238,
  serialized_end=414,
)


_AUTHGROUP = _descriptor.Descriptor(
  name='AuthGroup',
  full_name='components.auth.proto.replication.AuthGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='components.auth.proto.replication.AuthGroup.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='members', full_name='components.auth.proto.replication.AuthGroup.members', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='globs', full_name='components.auth.proto.replication.AuthGroup.globs', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nested', full_name='components.auth.proto.replication.AuthGroup.nested', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='components.auth.proto.replication.AuthGroup.description', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_ts', full_name='components.auth.proto.replication.AuthGroup.created_ts', index=5,
      number=6, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='components.auth.proto.replication.AuthGroup.created_by', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_ts', full_name='components.auth.proto.replication.AuthGroup.modified_ts', index=7,
      number=8, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_by', full_name='components.auth.proto.replication.AuthGroup.modified_by', index=8,
      number=9, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='owners', full_name='components.auth.proto.replication.AuthGroup.owners', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=417,
  serialized_end=609,
)


_AUTHSECRET = _descriptor.Descriptor(
  name='AuthSecret',
  full_name='components.auth.proto.replication.AuthSecret',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='components.auth.proto.replication.AuthSecret.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='components.auth.proto.replication.AuthSecret.values', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_ts', full_name='components.auth.proto.replication.AuthSecret.modified_ts', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_by', full_name='components.auth.proto.replication.AuthSecret.modified_by', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=611,
  serialized_end=695,
)


_AUTHIPWHITELIST = _descriptor.Descriptor(
  name='AuthIPWhitelist',
  full_name='components.auth.proto.replication.AuthIPWhitelist',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='components.auth.proto.replication.AuthIPWhitelist.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subnets', full_name='components.auth.proto.replication.AuthIPWhitelist.subnets', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='components.auth.proto.replication.AuthIPWhitelist.description', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_ts', full_name='components.auth.proto.replication.AuthIPWhitelist.created_ts', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='components.auth.proto.replication.AuthIPWhitelist.created_by', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_ts', full_name='components.auth.proto.replication.AuthIPWhitelist.modified_ts', index=5,
      number=6, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_by', full_name='components.auth.proto.replication.AuthIPWhitelist.modified_by', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=698,
  serialized_end=849,
)


_AUTHIPWHITELISTASSIGNMENT = _descriptor.Descriptor(
  name='AuthIPWhitelistAssignment',
  full_name='components.auth.proto.replication.AuthIPWhitelistAssignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='identity', full_name='components.auth.proto.replication.AuthIPWhitelistAssignment.identity', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_whitelist', full_name='components.auth.proto.replication.AuthIPWhitelistAssignment.ip_whitelist', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='comment', full_name='components.auth.proto.replication.AuthIPWhitelistAssignment.comment', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_ts', full_name='components.auth.proto.replication.AuthIPWhitelistAssignment.created_ts', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='components.auth.proto.replication.AuthIPWhitelistAssignment.created_by', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=851,
  serialized_end=975,
)


_AUTHDB = _descriptor.Descriptor(
  name='AuthDB',
  full_name='components.auth.proto.replication.AuthDB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='oauth_client_id', full_name='components.auth.proto.replication.AuthDB.oauth_client_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oauth_client_secret', full_name='components.auth.proto.replication.AuthDB.oauth_client_secret', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oauth_additional_client_ids', full_name='components.auth.proto.replication.AuthDB.oauth_additional_client_ids', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='groups', full_name='components.auth.proto.replication.AuthDB.groups', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='secrets', full_name='components.auth.proto.replication.AuthDB.secrets', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_whitelists', full_name='components.auth.proto.replication.AuthDB.ip_whitelists', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_whitelist_assignments', full_name='components.auth.proto.replication.AuthDB.ip_whitelist_assignments', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  extension_ranges=[],
  serialized_start=978,
  serialized_end=1374,
)


_AUTHDBREVISION = _descriptor.Descriptor(
  name='AuthDBRevision',
  full_name='components.auth.proto.replication.AuthDBRevision',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='primary_id', full_name='components.auth.proto.replication.AuthDBRevision.primary_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_db_rev', full_name='components.auth.proto.replication.AuthDBRevision.auth_db_rev', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modified_ts', full_name='components.auth.proto.replication.AuthDBRevision.modified_ts', index=2,
      number=3, type=3, cpp_type=2, label=2,
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
  extension_ranges=[],
  serialized_start=1376,
  serialized_end=1454,
)


_CHANGENOTIFICATION = _descriptor.Descriptor(
  name='ChangeNotification',
  full_name='components.auth.proto.replication.ChangeNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='revision', full_name='components.auth.proto.replication.ChangeNotification.revision', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  extension_ranges=[],
  serialized_start=1456,
  serialized_end=1545,
)


_REPLICATIONPUSHREQUEST = _descriptor.Descriptor(
  name='ReplicationPushRequest',
  full_name='components.auth.proto.replication.ReplicationPushRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='revision', full_name='components.auth.proto.replication.ReplicationPushRequest.revision', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_db', full_name='components.auth.proto.replication.ReplicationPushRequest.auth_db', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_code_version', full_name='components.auth.proto.replication.ReplicationPushRequest.auth_code_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=1548,
  serialized_end=1728,
)


_REPLICATIONPUSHRESPONSE = _descriptor.Descriptor(
  name='ReplicationPushResponse',
  full_name='components.auth.proto.replication.ReplicationPushResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='components.auth.proto.replication.ReplicationPushResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='current_revision', full_name='components.auth.proto.replication.ReplicationPushResponse.current_revision', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_code', full_name='components.auth.proto.replication.ReplicationPushResponse.error_code', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_code_version', full_name='components.auth.proto.replication.ReplicationPushResponse.auth_code_version', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REPLICATIONPUSHRESPONSE_STATUS,
    _REPLICATIONPUSHRESPONSE_ERRORCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1731,
  serialized_end=2213,
)

_SERVICELINKRESPONSE.fields_by_name['status'].enum_type = _SERVICELINKRESPONSE_STATUS
_SERVICELINKRESPONSE_STATUS.containing_type = _SERVICELINKRESPONSE;
_AUTHDB.fields_by_name['groups'].message_type = _AUTHGROUP
_AUTHDB.fields_by_name['secrets'].message_type = _AUTHSECRET
_AUTHDB.fields_by_name['ip_whitelists'].message_type = _AUTHIPWHITELIST
_AUTHDB.fields_by_name['ip_whitelist_assignments'].message_type = _AUTHIPWHITELISTASSIGNMENT
_CHANGENOTIFICATION.fields_by_name['revision'].message_type = _AUTHDBREVISION
_REPLICATIONPUSHREQUEST.fields_by_name['revision'].message_type = _AUTHDBREVISION
_REPLICATIONPUSHREQUEST.fields_by_name['auth_db'].message_type = _AUTHDB
_REPLICATIONPUSHRESPONSE.fields_by_name['status'].enum_type = _REPLICATIONPUSHRESPONSE_STATUS
_REPLICATIONPUSHRESPONSE.fields_by_name['current_revision'].message_type = _AUTHDBREVISION
_REPLICATIONPUSHRESPONSE.fields_by_name['error_code'].enum_type = _REPLICATIONPUSHRESPONSE_ERRORCODE
_REPLICATIONPUSHRESPONSE_STATUS.containing_type = _REPLICATIONPUSHRESPONSE;
_REPLICATIONPUSHRESPONSE_ERRORCODE.containing_type = _REPLICATIONPUSHRESPONSE;
DESCRIPTOR.message_types_by_name['ServiceLinkTicket'] = _SERVICELINKTICKET
DESCRIPTOR.message_types_by_name['ServiceLinkRequest'] = _SERVICELINKREQUEST
DESCRIPTOR.message_types_by_name['ServiceLinkResponse'] = _SERVICELINKRESPONSE
DESCRIPTOR.message_types_by_name['AuthGroup'] = _AUTHGROUP
DESCRIPTOR.message_types_by_name['AuthSecret'] = _AUTHSECRET
DESCRIPTOR.message_types_by_name['AuthIPWhitelist'] = _AUTHIPWHITELIST
DESCRIPTOR.message_types_by_name['AuthIPWhitelistAssignment'] = _AUTHIPWHITELISTASSIGNMENT
DESCRIPTOR.message_types_by_name['AuthDB'] = _AUTHDB
DESCRIPTOR.message_types_by_name['AuthDBRevision'] = _AUTHDBREVISION
DESCRIPTOR.message_types_by_name['ChangeNotification'] = _CHANGENOTIFICATION
DESCRIPTOR.message_types_by_name['ReplicationPushRequest'] = _REPLICATIONPUSHREQUEST
DESCRIPTOR.message_types_by_name['ReplicationPushResponse'] = _REPLICATIONPUSHRESPONSE

class ServiceLinkTicket(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVICELINKTICKET

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ServiceLinkTicket)

class ServiceLinkRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVICELINKREQUEST

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ServiceLinkRequest)

class ServiceLinkResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVICELINKRESPONSE

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ServiceLinkResponse)

class AuthGroup(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHGROUP

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthGroup)

class AuthSecret(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHSECRET

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthSecret)

class AuthIPWhitelist(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHIPWHITELIST

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthIPWhitelist)

class AuthIPWhitelistAssignment(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHIPWHITELISTASSIGNMENT

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthIPWhitelistAssignment)

class AuthDB(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHDB

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthDB)

class AuthDBRevision(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHDBREVISION

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.AuthDBRevision)

class ChangeNotification(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CHANGENOTIFICATION

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ChangeNotification)

class ReplicationPushRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REPLICATIONPUSHREQUEST

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ReplicationPushRequest)

class ReplicationPushResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REPLICATIONPUSHRESPONSE

  # @@protoc_insertion_point(class_scope:components.auth.proto.replication.ReplicationPushResponse)


# @@protoc_insertion_point(module_scope)
