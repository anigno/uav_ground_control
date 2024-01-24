import logging
from logging import Logger
from threading import Thread
import grpc
from concurrent import futures
from Apps.uav_simulator.simulator.communication.grpc import communication_service_pb2_grpc
from common.generic_event import GenericEvent
from Apps.uav_simulator.simulator.communication.grpc.communication_service_pb2 import pStatusUpdate, pFlyToDestination, pResponse
from Apps.uav_simulator.simulator.communication.grpc.communication_service_pb2_grpc import CommunicationServiceServicer, add_CommunicationServiceServicer_to_server
from logging_provider.logging_initiator_by_code import LoggingInitiatorByCode

class GrpcMessagesServer(CommunicationServiceServicer):
    """grpc service running remote procedures and raising events"""

    def __init__(self, logger: Logger, ip, port):
        self._logger = logger
        self._service_ip = ip
        self._service_port = port
        self._server_thread = None
        self.on_StatusUpdateRequest = GenericEvent(pStatusUpdate)
        self.on_FlyToDestinationRequest = GenericEvent(pFlyToDestination)

    def StatusUpdateRequest(self, proto_status_update: pStatusUpdate, context):
        """grpc request handler, shouldn't be called directly"""
        self._logger.debug(f"Received StatusUpdateRequest: {proto_status_update}")
        response = pResponse(response_string="StatusUpdateRequest received")
        self.on_StatusUpdateRequest.raise_event(proto_status_update)
        return response

    def FlyToDestinationRequest(self, proto_fly_to_destination: pFlyToDestination, context):
        """grpc request handler, shouldn't be called directly"""
        self._logger.debug(f"Received FlyToDestinationRequest: {proto_fly_to_destination}")
        response = pResponse(response_string="FlyToDestinationRequest received")
        self.on_FlyToDestinationRequest.raise_event(proto_fly_to_destination)
        return response

    def _serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        communication_service_pb2_grpc.add_CommunicationServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{self._service_ip}:{self._service_port}')
        # server.add_secure_port(f'{self.ip}:{self.port}',grpc.ssl_server_credentials(()))
        server.start()
        self._logger.debug(f"GrpcMessagesServer started at: {self._service_ip}:{self._service_port}")
        server.wait_for_termination()

    def start(self):
        """start receiving requests"""
        self._server_thread = Thread(name='GrpcMessagesServer', target=self._serve, daemon=True)
        self._server_thread.start()

if __name__ == '__main__':
    logger1: Logger = logging.getLogger(LoggingInitiatorByCode.FILE_SYSTEM_LOGGER)
    LoggingInitiatorByCode()

    message_server = GrpcMessagesServer(logger1, 'localhost', 50052)
    message_server.start()
    input('exit')
