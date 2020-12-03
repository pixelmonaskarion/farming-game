# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import farmServerMethods_pb2 as farmServerMethods__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class FarmingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMap = channel.unary_unary(
                '/farming.Farming/GetMap',
                request_serializer=farmServerMethods__pb2.Coords.SerializeToString,
                response_deserializer=farmServerMethods__pb2.Map.FromString,
                )
        self.GetItems = channel.unary_unary(
                '/farming.Farming/GetItems',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=farmServerMethods__pb2.Items.FromString,
                )
        self.GetPlayers = channel.unary_unary(
                '/farming.Farming/GetPlayers',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=farmServerMethods__pb2.Players.FromString,
                )
        self.SendPlayer = channel.unary_unary(
                '/farming.Farming/SendPlayer',
                request_serializer=farmServerMethods__pb2.Player.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.PlayerLeave = channel.unary_unary(
                '/farming.Farming/PlayerLeave',
                request_serializer=farmServerMethods__pb2.Player.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.DeleteItems = channel.unary_unary(
                '/farming.Farming/DeleteItems',
                request_serializer=farmServerMethods__pb2.Item.SerializeToString,
                response_deserializer=farmServerMethods__pb2.Item.FromString,
                )
        self.changeStuff = channel.unary_unary(
                '/farming.Farming/changeStuff',
                request_serializer=farmServerMethods__pb2.MapUpdate.SerializeToString,
                response_deserializer=farmServerMethods__pb2.Map.FromString,
                )


class FarmingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMap(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlayers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendPlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PlayerLeave(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def changeStuff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FarmingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMap': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMap,
                    request_deserializer=farmServerMethods__pb2.Coords.FromString,
                    response_serializer=farmServerMethods__pb2.Map.SerializeToString,
            ),
            'GetItems': grpc.unary_unary_rpc_method_handler(
                    servicer.GetItems,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=farmServerMethods__pb2.Items.SerializeToString,
            ),
            'GetPlayers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlayers,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=farmServerMethods__pb2.Players.SerializeToString,
            ),
            'SendPlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.SendPlayer,
                    request_deserializer=farmServerMethods__pb2.Player.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'PlayerLeave': grpc.unary_unary_rpc_method_handler(
                    servicer.PlayerLeave,
                    request_deserializer=farmServerMethods__pb2.Player.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DeleteItems': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteItems,
                    request_deserializer=farmServerMethods__pb2.Item.FromString,
                    response_serializer=farmServerMethods__pb2.Item.SerializeToString,
            ),
            'changeStuff': grpc.unary_unary_rpc_method_handler(
                    servicer.changeStuff,
                    request_deserializer=farmServerMethods__pb2.MapUpdate.FromString,
                    response_serializer=farmServerMethods__pb2.Map.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'farming.Farming', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Farming(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMap(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/GetMap',
            farmServerMethods__pb2.Coords.SerializeToString,
            farmServerMethods__pb2.Map.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/GetItems',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            farmServerMethods__pb2.Items.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPlayers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/GetPlayers',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            farmServerMethods__pb2.Players.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendPlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/SendPlayer',
            farmServerMethods__pb2.Player.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PlayerLeave(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/PlayerLeave',
            farmServerMethods__pb2.Player.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/DeleteItems',
            farmServerMethods__pb2.Item.SerializeToString,
            farmServerMethods__pb2.Item.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def changeStuff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/farming.Farming/changeStuff',
            farmServerMethods__pb2.MapUpdate.SerializeToString,
            farmServerMethods__pb2.Map.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
