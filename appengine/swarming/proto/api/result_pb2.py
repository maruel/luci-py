# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: result.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='result.proto',
  package='test_platform.skylab_test_runner',
  syntax='proto3',
  serialized_options=_b('ZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_test_runner'),
  serialized_pb=_b('\n\x0cresult.proto\x12 test_platform.skylab_test_runner\"\x88\x03\n\x06Result\x12L\n\x0f\x61utotest_result\x18\x01 \x01(\x0b\x32\x31.test_platform.skylab_test_runner.Result.AutotestH\x00\x1a\xa4\x02\n\x08\x41utotest\x12N\n\ntest_cases\x18\x01 \x03(\x0b\x32:.test_platform.skylab_test_runner.Result.Autotest.TestCase\x12\x12\n\nincomplete\x18\x02 \x01(\x08\x1a\xb3\x01\n\x08TestCase\x12\x0c\n\x04name\x18\x01 \x01(\t\x12S\n\x07verdict\x18\x02 \x01(\x0e\x32\x42.test_platform.skylab_test_runner.Result.Autotest.TestCase.Verdict\"D\n\x07Verdict\x12\x15\n\x11VERDICT_UNDEFINED\x10\x00\x12\x10\n\x0cVERDICT_PASS\x10\x01\x12\x10\n\x0cVERDICT_FAIL\x10\x02\x42\t\n\x07harnessBLZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_test_runnerb\x06proto3')
)



_RESULT_AUTOTEST_TESTCASE_VERDICT = _descriptor.EnumDescriptor(
  name='Verdict',
  full_name='test_platform.skylab_test_runner.Result.Autotest.TestCase.Verdict',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VERDICT_UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERDICT_PASS', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERDICT_FAIL', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=364,
  serialized_end=432,
)
_sym_db.RegisterEnumDescriptor(_RESULT_AUTOTEST_TESTCASE_VERDICT)


_RESULT_AUTOTEST_TESTCASE = _descriptor.Descriptor(
  name='TestCase',
  full_name='test_platform.skylab_test_runner.Result.Autotest.TestCase',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test_platform.skylab_test_runner.Result.Autotest.TestCase.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verdict', full_name='test_platform.skylab_test_runner.Result.Autotest.TestCase.verdict', index=1,
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
    _RESULT_AUTOTEST_TESTCASE_VERDICT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=432,
)

_RESULT_AUTOTEST = _descriptor.Descriptor(
  name='Autotest',
  full_name='test_platform.skylab_test_runner.Result.Autotest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_cases', full_name='test_platform.skylab_test_runner.Result.Autotest.test_cases', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='incomplete', full_name='test_platform.skylab_test_runner.Result.Autotest.incomplete', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RESULT_AUTOTEST_TESTCASE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=140,
  serialized_end=432,
)

_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='test_platform.skylab_test_runner.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='autotest_result', full_name='test_platform.skylab_test_runner.Result.autotest_result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RESULT_AUTOTEST, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='harness', full_name='test_platform.skylab_test_runner.Result.harness',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=51,
  serialized_end=443,
)

_RESULT_AUTOTEST_TESTCASE.fields_by_name['verdict'].enum_type = _RESULT_AUTOTEST_TESTCASE_VERDICT
_RESULT_AUTOTEST_TESTCASE.containing_type = _RESULT_AUTOTEST
_RESULT_AUTOTEST_TESTCASE_VERDICT.containing_type = _RESULT_AUTOTEST_TESTCASE
_RESULT_AUTOTEST.fields_by_name['test_cases'].message_type = _RESULT_AUTOTEST_TESTCASE
_RESULT_AUTOTEST.containing_type = _RESULT
_RESULT.fields_by_name['autotest_result'].message_type = _RESULT_AUTOTEST
_RESULT.oneofs_by_name['harness'].fields.append(
  _RESULT.fields_by_name['autotest_result'])
_RESULT.fields_by_name['autotest_result'].containing_oneof = _RESULT.oneofs_by_name['harness']
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(

  Autotest = _reflection.GeneratedProtocolMessageType('Autotest', (_message.Message,), dict(

    TestCase = _reflection.GeneratedProtocolMessageType('TestCase', (_message.Message,), dict(
      DESCRIPTOR = _RESULT_AUTOTEST_TESTCASE,
      __module__ = 'result_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.skylab_test_runner.Result.Autotest.TestCase)
      ))
    ,
    DESCRIPTOR = _RESULT_AUTOTEST,
    __module__ = 'result_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.skylab_test_runner.Result.Autotest)
    ))
  ,
  DESCRIPTOR = _RESULT,
  __module__ = 'result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.skylab_test_runner.Result)
  ))
_sym_db.RegisterMessage(Result)
_sym_db.RegisterMessage(Result.Autotest)
_sym_db.RegisterMessage(Result.Autotest.TestCase)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
