# Generated by the pRPC protocol buffer compiler plugin.  DO NOT EDIT!
# source: swarming.proto

import base64
import zlib

from google.protobuf import descriptor_pb2

# Includes description of the swarming.proto and all of its transitive
# dependencies. Includes source code info.
FILE_DESCRIPTOR_SET = descriptor_pb2.FileDescriptorSet()
FILE_DESCRIPTOR_SET.ParseFromString(zlib.decompress(base64.b64decode(
    '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')))
_INDEX = {
    f.name: {
      'descriptor': f,
      'services': {s.name: s for s in f.service},
    }
    for f in FILE_DESCRIPTOR_SET.file
}


BotAPIServiceDescription = {
  'file_descriptor_set': FILE_DESCRIPTOR_SET,
  'file_descriptor': _INDEX[u'swarming.proto']['descriptor'],
  'service_descriptor': _INDEX[u'swarming.proto']['services'][u'BotAPI'],
}
