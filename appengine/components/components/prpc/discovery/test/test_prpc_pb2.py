# Generated by the pRPC protocol buffer compiler plugin.  DO NOT EDIT!
# source: test.proto

import base64
import zlib

from google.protobuf import descriptor_pb2

# Includes description of the test.proto and all of its transitive
# dependencies. Includes source code info.
FILE_DESCRIPTOR_SET = descriptor_pb2.FileDescriptorSet()
FILE_DESCRIPTOR_SET.ParseFromString(zlib.decompress(base64.b64decode(
    'eJzdUj1v01AUjZ2Pvly75tUUNakAXYWFobJSAxJriFqRqGJIG9YqtV8aS8Ev2E7V/h1GBjYY2P'
    'lTTFy/2LETtQNrt3vOu1/vngPf6gCJiBNnEclE2pYfxJ68EdHdZcoe7gdfFjJKhH98WWR1LDA/'
    'ivlcjsTXJbGdU9jNcLyQYSzsd8DywpaG2mvDbTubnZ1B3ni0TnXHYFzQ27mIbgJP2KdQV23t59'
    'vF5emHLx54Xe3SqQx/VYHxGq/wPa7BT42ZCtjudw37cnEXBdezBN3u8Xu8mAk8G/cH2FsmMxnF'
    'Dvbmc1QJMUYipsWE7wCOY4FyisksiDGWy8gT6ElfIMHrdJFQ+LgMfRFRisDeYuKljelPtNARfh'
    'ZRHMgQXacLlDBJ0JuEeCVwKqkIg1BVnQ36J5/OT3AazIUDwJjOG7T2AYVVVuGM4pdgsgbFQLFJ'
    'f1OIaYQZfwqWQjq9G1znb4nMMGUY1MsoMToxJm+VmCoxr3iXptWog6Umm2lM1Rb131dI40+yuy'
    'qkMOPPaHaK0tmcZrepb4ZZQzFGidGIMalfwVSJOeCtq4ay2xv4U4V7jfiwXd2yXT9Ac+22/7Gm'
    'W1hz+FvPPGQ+Qg/VNjxUW3toT+lYeGilYyXT0VjrWLgq17HwUFnHvzrcq9C2jp12oZhrm6DdKq'
    'nqI+12+CMXAh6FEKvjs+w/+fHZ1vGbdGqrdNi6YnY2jt+kmubG8Zskx25+/H8t6V9E')))
_INDEX = {
    f.name: {
      'descriptor': f,
      'services': {s.name: s for s in f.service},
    }
    for f in FILE_DESCRIPTOR_SET.file
}


TestServiceServiceDescription = {
  'file_descriptor_set': FILE_DESCRIPTOR_SET,
  'file_descriptor': _INDEX[u'test.proto']['descriptor'],
  'service_descriptor': _INDEX[u'test.proto']['services'][u'TestService'],
}
