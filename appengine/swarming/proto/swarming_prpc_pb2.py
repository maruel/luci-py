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
