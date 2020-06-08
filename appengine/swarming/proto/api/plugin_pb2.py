# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plugin.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import swarming_pb2 as swarming__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='plugin.proto',
  package='swarming.v1',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/luci/swarming/proto/api;apipb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cplugin.proto\x12\x0bswarming.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0eswarming.proto\"\xb6\x01\n\x08TaskSpec\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04tags\x18\x02 \x03(\t\x12&\n\x06slices\x18\x03 \x03(\x0b\x32\x16.swarming.v1.SliceSpec\x12%\n\x05state\x18\x04 \x01(\x0e\x32\x16.swarming.v1.TaskState\x12\x0e\n\x06\x62ot_id\x18\x05 \x01(\t\x12\x31\n\renqueued_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x1f\n\tSliceSpec\x12\x12\n\ndimensions\x18\x01 \x03(\t\"-\n\x07IdleBot\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\t\x12\x12\n\ndimensions\x18\x02 \x03(\t\"}\n\x12\x41ssignTasksRequest\x12\x14\n\x0cscheduler_id\x18\x01 \x01(\t\x12\'\n\tidle_bots\x18\x02 \x03(\x0b\x32\x14.swarming.v1.IdleBot\x12(\n\x04time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"G\n\x13\x41ssignTasksResponse\x12\x30\n\x0b\x61ssignments\x18\x01 \x03(\x0b\x32\x1b.swarming.v1.TaskAssignment\"G\n\x0eTaskAssignment\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\t\x12\x0f\n\x07task_id\x18\x02 \x01(\t\x12\x14\n\x0cslice_number\x18\x03 \x01(\x05\"/\n\x17GetCancellationsRequest\x12\x14\n\x0cscheduler_id\x18\x01 \x01(\t\"\xa7\x02\n\x18GetCancellationsResponse\x12I\n\rcancellations\x18\x01 \x03(\x0b\x32\x32.swarming.v1.GetCancellationsResponse.Cancellation\x1a\xbf\x01\n\x0c\x43\x61ncellation\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\t\x12\x0f\n\x07task_id\x18\x02 \x01(\t\x12I\n\x06reason\x18\x03 \x01(\x0e\x32\x39.swarming.v1.GetCancellationsResponse.Cancellation.Reason\x12\x12\n\nextra_info\x18\x04 \x01(\t\"/\n\x06Reason\x12\x0b\n\x07INVALID\x10\x00\x12\r\n\tPREEMPTED\x10\x01\x12\t\n\x05\x45RROR\x10\x02\"`\n\x0fNotifyTasksItem\x12(\n\x04time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12#\n\x04task\x18\x02 \x01(\x0b\x32\x15.swarming.v1.TaskSpec\"t\n\x12NotifyTasksRequest\x12\x14\n\x0cscheduler_id\x18\x01 \x01(\t\x12\x33\n\rnotifications\x18\x02 \x03(\x0b\x32\x1c.swarming.v1.NotifyTasksItem\x12\x13\n\x0bis_callback\x18\x03 \x01(\x08\"\x15\n\x13NotifyTasksResponse\"+\n\x13GetCallbacksRequest\x12\x14\n\x0cscheduler_id\x18\x01 \x01(\t\"(\n\x14GetCallbacksResponse\x12\x10\n\x08task_ids\x18\x01 \x03(\t2\xed\x02\n\x11\x45xternalScheduler\x12P\n\x0b\x41ssignTasks\x12\x1f.swarming.v1.AssignTasksRequest\x1a .swarming.v1.AssignTasksResponse\x12_\n\x10GetCancellations\x12$.swarming.v1.GetCancellationsRequest\x1a%.swarming.v1.GetCancellationsResponse\x12P\n\x0bNotifyTasks\x12\x1f.swarming.v1.NotifyTasksRequest\x1a .swarming.v1.NotifyTasksResponse\x12S\n\x0cGetCallbacks\x12 .swarming.v1.GetCallbacksRequest\x1a!.swarming.v1.GetCallbacksResponseB/Z-go.chromium.org/luci/swarming/proto/api;apipbb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,swarming__pb2.DESCRIPTOR,])



_GETCANCELLATIONSRESPONSE_CANCELLATION_REASON = _descriptor.EnumDescriptor(
  name='Reason',
  full_name='swarming.v1.GetCancellationsResponse.Cancellation.Reason',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INVALID', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PREEMPTED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=914,
  serialized_end=961,
)
_sym_db.RegisterEnumDescriptor(_GETCANCELLATIONSRESPONSE_CANCELLATION_REASON)


_TASKSPEC = _descriptor.Descriptor(
  name='TaskSpec',
  full_name='swarming.v1.TaskSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='swarming.v1.TaskSpec.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='swarming.v1.TaskSpec.tags', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='slices', full_name='swarming.v1.TaskSpec.slices', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='swarming.v1.TaskSpec.state', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='swarming.v1.TaskSpec.bot_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enqueued_time', full_name='swarming.v1.TaskSpec.enqueued_time', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=79,
  serialized_end=261,
)


_SLICESPEC = _descriptor.Descriptor(
  name='SliceSpec',
  full_name='swarming.v1.SliceSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='swarming.v1.SliceSpec.dimensions', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=263,
  serialized_end=294,
)


_IDLEBOT = _descriptor.Descriptor(
  name='IdleBot',
  full_name='swarming.v1.IdleBot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='swarming.v1.IdleBot.bot_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='swarming.v1.IdleBot.dimensions', index=1,
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
  serialized_start=296,
  serialized_end=341,
)


_ASSIGNTASKSREQUEST = _descriptor.Descriptor(
  name='AssignTasksRequest',
  full_name='swarming.v1.AssignTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduler_id', full_name='swarming.v1.AssignTasksRequest.scheduler_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='idle_bots', full_name='swarming.v1.AssignTasksRequest.idle_bots', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='swarming.v1.AssignTasksRequest.time', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=343,
  serialized_end=468,
)


_ASSIGNTASKSRESPONSE = _descriptor.Descriptor(
  name='AssignTasksResponse',
  full_name='swarming.v1.AssignTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='assignments', full_name='swarming.v1.AssignTasksResponse.assignments', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=470,
  serialized_end=541,
)


_TASKASSIGNMENT = _descriptor.Descriptor(
  name='TaskAssignment',
  full_name='swarming.v1.TaskAssignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='swarming.v1.TaskAssignment.bot_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_id', full_name='swarming.v1.TaskAssignment.task_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='slice_number', full_name='swarming.v1.TaskAssignment.slice_number', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=543,
  serialized_end=614,
)


_GETCANCELLATIONSREQUEST = _descriptor.Descriptor(
  name='GetCancellationsRequest',
  full_name='swarming.v1.GetCancellationsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduler_id', full_name='swarming.v1.GetCancellationsRequest.scheduler_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=616,
  serialized_end=663,
)


_GETCANCELLATIONSRESPONSE_CANCELLATION = _descriptor.Descriptor(
  name='Cancellation',
  full_name='swarming.v1.GetCancellationsResponse.Cancellation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot_id', full_name='swarming.v1.GetCancellationsResponse.Cancellation.bot_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_id', full_name='swarming.v1.GetCancellationsResponse.Cancellation.task_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reason', full_name='swarming.v1.GetCancellationsResponse.Cancellation.reason', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extra_info', full_name='swarming.v1.GetCancellationsResponse.Cancellation.extra_info', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GETCANCELLATIONSRESPONSE_CANCELLATION_REASON,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=770,
  serialized_end=961,
)

_GETCANCELLATIONSRESPONSE = _descriptor.Descriptor(
  name='GetCancellationsResponse',
  full_name='swarming.v1.GetCancellationsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cancellations', full_name='swarming.v1.GetCancellationsResponse.cancellations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_GETCANCELLATIONSRESPONSE_CANCELLATION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=666,
  serialized_end=961,
)


_NOTIFYTASKSITEM = _descriptor.Descriptor(
  name='NotifyTasksItem',
  full_name='swarming.v1.NotifyTasksItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='swarming.v1.NotifyTasksItem.time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task', full_name='swarming.v1.NotifyTasksItem.task', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=963,
  serialized_end=1059,
)


_NOTIFYTASKSREQUEST = _descriptor.Descriptor(
  name='NotifyTasksRequest',
  full_name='swarming.v1.NotifyTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduler_id', full_name='swarming.v1.NotifyTasksRequest.scheduler_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='notifications', full_name='swarming.v1.NotifyTasksRequest.notifications', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_callback', full_name='swarming.v1.NotifyTasksRequest.is_callback', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=1061,
  serialized_end=1177,
)


_NOTIFYTASKSRESPONSE = _descriptor.Descriptor(
  name='NotifyTasksResponse',
  full_name='swarming.v1.NotifyTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1179,
  serialized_end=1200,
)


_GETCALLBACKSREQUEST = _descriptor.Descriptor(
  name='GetCallbacksRequest',
  full_name='swarming.v1.GetCallbacksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduler_id', full_name='swarming.v1.GetCallbacksRequest.scheduler_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=1202,
  serialized_end=1245,
)


_GETCALLBACKSRESPONSE = _descriptor.Descriptor(
  name='GetCallbacksResponse',
  full_name='swarming.v1.GetCallbacksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_ids', full_name='swarming.v1.GetCallbacksResponse.task_ids', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=1247,
  serialized_end=1287,
)

_TASKSPEC.fields_by_name['slices'].message_type = _SLICESPEC
_TASKSPEC.fields_by_name['state'].enum_type = swarming__pb2._TASKSTATE
_TASKSPEC.fields_by_name['enqueued_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_ASSIGNTASKSREQUEST.fields_by_name['idle_bots'].message_type = _IDLEBOT
_ASSIGNTASKSREQUEST.fields_by_name['time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_ASSIGNTASKSRESPONSE.fields_by_name['assignments'].message_type = _TASKASSIGNMENT
_GETCANCELLATIONSRESPONSE_CANCELLATION.fields_by_name['reason'].enum_type = _GETCANCELLATIONSRESPONSE_CANCELLATION_REASON
_GETCANCELLATIONSRESPONSE_CANCELLATION.containing_type = _GETCANCELLATIONSRESPONSE
_GETCANCELLATIONSRESPONSE_CANCELLATION_REASON.containing_type = _GETCANCELLATIONSRESPONSE_CANCELLATION
_GETCANCELLATIONSRESPONSE.fields_by_name['cancellations'].message_type = _GETCANCELLATIONSRESPONSE_CANCELLATION
_NOTIFYTASKSITEM.fields_by_name['time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_NOTIFYTASKSITEM.fields_by_name['task'].message_type = _TASKSPEC
_NOTIFYTASKSREQUEST.fields_by_name['notifications'].message_type = _NOTIFYTASKSITEM
DESCRIPTOR.message_types_by_name['TaskSpec'] = _TASKSPEC
DESCRIPTOR.message_types_by_name['SliceSpec'] = _SLICESPEC
DESCRIPTOR.message_types_by_name['IdleBot'] = _IDLEBOT
DESCRIPTOR.message_types_by_name['AssignTasksRequest'] = _ASSIGNTASKSREQUEST
DESCRIPTOR.message_types_by_name['AssignTasksResponse'] = _ASSIGNTASKSRESPONSE
DESCRIPTOR.message_types_by_name['TaskAssignment'] = _TASKASSIGNMENT
DESCRIPTOR.message_types_by_name['GetCancellationsRequest'] = _GETCANCELLATIONSREQUEST
DESCRIPTOR.message_types_by_name['GetCancellationsResponse'] = _GETCANCELLATIONSRESPONSE
DESCRIPTOR.message_types_by_name['NotifyTasksItem'] = _NOTIFYTASKSITEM
DESCRIPTOR.message_types_by_name['NotifyTasksRequest'] = _NOTIFYTASKSREQUEST
DESCRIPTOR.message_types_by_name['NotifyTasksResponse'] = _NOTIFYTASKSRESPONSE
DESCRIPTOR.message_types_by_name['GetCallbacksRequest'] = _GETCALLBACKSREQUEST
DESCRIPTOR.message_types_by_name['GetCallbacksResponse'] = _GETCALLBACKSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskSpec = _reflection.GeneratedProtocolMessageType('TaskSpec', (_message.Message,), {
  'DESCRIPTOR' : _TASKSPEC,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.TaskSpec)
  })
_sym_db.RegisterMessage(TaskSpec)

SliceSpec = _reflection.GeneratedProtocolMessageType('SliceSpec', (_message.Message,), {
  'DESCRIPTOR' : _SLICESPEC,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.SliceSpec)
  })
_sym_db.RegisterMessage(SliceSpec)

IdleBot = _reflection.GeneratedProtocolMessageType('IdleBot', (_message.Message,), {
  'DESCRIPTOR' : _IDLEBOT,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.IdleBot)
  })
_sym_db.RegisterMessage(IdleBot)

AssignTasksRequest = _reflection.GeneratedProtocolMessageType('AssignTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _ASSIGNTASKSREQUEST,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.AssignTasksRequest)
  })
_sym_db.RegisterMessage(AssignTasksRequest)

AssignTasksResponse = _reflection.GeneratedProtocolMessageType('AssignTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _ASSIGNTASKSRESPONSE,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.AssignTasksResponse)
  })
_sym_db.RegisterMessage(AssignTasksResponse)

TaskAssignment = _reflection.GeneratedProtocolMessageType('TaskAssignment', (_message.Message,), {
  'DESCRIPTOR' : _TASKASSIGNMENT,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.TaskAssignment)
  })
_sym_db.RegisterMessage(TaskAssignment)

GetCancellationsRequest = _reflection.GeneratedProtocolMessageType('GetCancellationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCANCELLATIONSREQUEST,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.GetCancellationsRequest)
  })
_sym_db.RegisterMessage(GetCancellationsRequest)

GetCancellationsResponse = _reflection.GeneratedProtocolMessageType('GetCancellationsResponse', (_message.Message,), {

  'Cancellation' : _reflection.GeneratedProtocolMessageType('Cancellation', (_message.Message,), {
    'DESCRIPTOR' : _GETCANCELLATIONSRESPONSE_CANCELLATION,
    '__module__' : 'plugin_pb2'
    # @@protoc_insertion_point(class_scope:swarming.v1.GetCancellationsResponse.Cancellation)
    })
  ,
  'DESCRIPTOR' : _GETCANCELLATIONSRESPONSE,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.GetCancellationsResponse)
  })
_sym_db.RegisterMessage(GetCancellationsResponse)
_sym_db.RegisterMessage(GetCancellationsResponse.Cancellation)

NotifyTasksItem = _reflection.GeneratedProtocolMessageType('NotifyTasksItem', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFYTASKSITEM,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.NotifyTasksItem)
  })
_sym_db.RegisterMessage(NotifyTasksItem)

NotifyTasksRequest = _reflection.GeneratedProtocolMessageType('NotifyTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFYTASKSREQUEST,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.NotifyTasksRequest)
  })
_sym_db.RegisterMessage(NotifyTasksRequest)

NotifyTasksResponse = _reflection.GeneratedProtocolMessageType('NotifyTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFYTASKSRESPONSE,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.NotifyTasksResponse)
  })
_sym_db.RegisterMessage(NotifyTasksResponse)

GetCallbacksRequest = _reflection.GeneratedProtocolMessageType('GetCallbacksRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCALLBACKSREQUEST,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.GetCallbacksRequest)
  })
_sym_db.RegisterMessage(GetCallbacksRequest)

GetCallbacksResponse = _reflection.GeneratedProtocolMessageType('GetCallbacksResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCALLBACKSRESPONSE,
  '__module__' : 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:swarming.v1.GetCallbacksResponse)
  })
_sym_db.RegisterMessage(GetCallbacksResponse)


DESCRIPTOR._options = None

_EXTERNALSCHEDULER = _descriptor.ServiceDescriptor(
  name='ExternalScheduler',
  full_name='swarming.v1.ExternalScheduler',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1290,
  serialized_end=1655,
  methods=[
  _descriptor.MethodDescriptor(
    name='AssignTasks',
    full_name='swarming.v1.ExternalScheduler.AssignTasks',
    index=0,
    containing_service=None,
    input_type=_ASSIGNTASKSREQUEST,
    output_type=_ASSIGNTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCancellations',
    full_name='swarming.v1.ExternalScheduler.GetCancellations',
    index=1,
    containing_service=None,
    input_type=_GETCANCELLATIONSREQUEST,
    output_type=_GETCANCELLATIONSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='NotifyTasks',
    full_name='swarming.v1.ExternalScheduler.NotifyTasks',
    index=2,
    containing_service=None,
    input_type=_NOTIFYTASKSREQUEST,
    output_type=_NOTIFYTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCallbacks',
    full_name='swarming.v1.ExternalScheduler.GetCallbacks',
    index=3,
    containing_service=None,
    input_type=_GETCALLBACKSREQUEST,
    output_type=_GETCALLBACKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EXTERNALSCHEDULER)

DESCRIPTOR.services_by_name['ExternalScheduler'] = _EXTERNALSCHEDULER

# @@protoc_insertion_point(module_scope)
