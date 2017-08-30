# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import task_manager_pb2 as task__manager__pb2


class TaskManagerStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetNextTask = channel.unary_unary(
        '/google.internal.devtools.workerfarm.v1test1.TaskManager/GetNextTask',
        request_serializer=task__manager__pb2.GetNextTaskRequest.SerializeToString,
        response_deserializer=task__manager__pb2.GetNextTaskResponse.FromString,
        )
    self.SyncTask = channel.unary_unary(
        '/google.internal.devtools.workerfarm.v1test1.TaskManager/SyncTask',
        request_serializer=task__manager__pb2.SyncTaskRequest.SerializeToString,
        response_deserializer=task__manager__pb2.SyncTaskResponse.FromString,
        )
    self.CompleteTask = channel.unary_unary(
        '/google.internal.devtools.workerfarm.v1test1.TaskManager/CompleteTask',
        request_serializer=task__manager__pb2.CompleteTaskRequest.SerializeToString,
        response_deserializer=task__manager__pb2.CompleteTaskResponse.FromString,
        )


class TaskManagerServicer(object):

  def GetNextTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SyncTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CompleteTask(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TaskManagerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetNextTask': grpc.unary_unary_rpc_method_handler(
          servicer.GetNextTask,
          request_deserializer=task__manager__pb2.GetNextTaskRequest.FromString,
          response_serializer=task__manager__pb2.GetNextTaskResponse.SerializeToString,
      ),
      'SyncTask': grpc.unary_unary_rpc_method_handler(
          servicer.SyncTask,
          request_deserializer=task__manager__pb2.SyncTaskRequest.FromString,
          response_serializer=task__manager__pb2.SyncTaskResponse.SerializeToString,
      ),
      'CompleteTask': grpc.unary_unary_rpc_method_handler(
          servicer.CompleteTask,
          request_deserializer=task__manager__pb2.CompleteTaskRequest.FromString,
          response_serializer=task__manager__pb2.CompleteTaskResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.internal.devtools.workerfarm.v1test1.TaskManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
