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
