import logging
import threading
import time
from enum import Enum
from http.client import HTTPResponse
from logging import Logger

from common.logging_provider.logging_initiator_by_code import LoggingInitiatorByCode
from common.utils.generic_event import GenericEvent
from common.utils.printable_params import PrintableParams
from uav_simulator.communication.http2.http2_client import Http2Client
from uav_simulator.communication.http2.http2_server import Http2Server
from uav_simulator.communication.messages.message_base import MessageBase
from uav_simulator.communication.messages.message_sent_fail_args import MessageSentFailsArgs
from uav_simulator.communication.messages_factory_base import MessagesFactoryBase

class Http2Communicator:
    """sends and receives messages based on MessageBase, using http2 client and server"""

    def __init__(self, logger: Logger, messages_factory: MessagesFactoryBase, local_ip: str, local_port: int):
        self.logger = logger
        self.messages_factory = messages_factory
        self.local_ip = local_ip
        self.local_port = local_port
        self.server = Http2Server
        self.client = Http2Client
        self.on_message_receive = GenericEvent(MessageBase)
        self.server.on_request_post_received += self._on_request_post_received
        self.on_error_sending_message = GenericEvent(MessageSentFailsArgs)

    def start(self):
        threading.Thread(target=lambda: self.server.start(self.local_ip, self.local_port), daemon=True).start()

    def send_message(self, message: MessageBase, ip, port) -> HTTPResponse:
        try:
            message.send_time = time.time()
            message_bytes = message.to_buffer()
            message_type_bytes = message.MESSAGE_TYPE.value.to_bytes(2, 'big', signed=False)
            message_bytes = message_type_bytes + message_bytes
            response = self.client.send_data_request(message_bytes, ip, port)
            return response
        except ConnectionRefusedError as ex:
            self.logger.debug(f'Message: {message.MESSAGE_TYPE} id: {message.message_id} to {ip}:{port} failed to sent')
            args = MessageSentFailsArgs(ex, message, f'{ip}:{port}')
            self.on_error_sending_message.raise_event(args)
        except Exception as ex:
            self.logger.exception('', ex)
            self.logger.debug(f'Message: {message.MESSAGE_TYPE} id: {message.message_id} to {ip}:{port} failed to sent')
            args = MessageSentFailsArgs(ex, message, f'{ip}:{port}')
            self.on_error_sending_message.raise_event(args)

    def _on_request_post_received(self, data_bytes: bytes):
        message_type_value = int.from_bytes(data_bytes[0:2], 'big', signed=False)
        message = self.messages_factory.create_message_instance(message_type_value, data_bytes[2:])
        self.on_message_receive.raise_event(message)

if __name__ == '__main__':
    from threading import Thread

    logger1: Logger = logging.getLogger(LoggingInitiatorByCode.FILE_SYSTEM_LOGGER)
    LoggingInitiatorByCode()

    class MessagesEnumTest(Enum):
        TEST_ENUM = 2222

    class TestMessage(MessageBase):
        MESSAGE_TYPE = MessagesEnumTest.TEST_ENUM

        def __init__(self):
            super().__init__()
            self.data = 'hello'

    class MessagesFactoryMock(MessagesFactoryBase):
        def init_messages(self):
            self.register_message(TestMessage)

        def __init__(self, logger):
            super().__init__(logger)

    mf = MessagesFactoryMock(logger1)

    def comm1_on_message_received(message):
        PrintableParams.print(message, header='* received')

    def server_comm_start():
        comm1 = Http2Communicator(logger1, mf, 'localhost', 1001)
        comm1.on_message_receive += comm1_on_message_received
        comm1.start()

    def client_comm_start():
        comm2 = Http2Communicator(logger1, mf, 'localhost', 1002)
        m = TestMessage()
        PrintableParams.print(m, header='+ sent')
        comm2.send_message(m, 'localhost', 1001)
        m = TestMessage()
        PrintableParams.print(m, header='sent')
        comm2.send_message(m, 'localhost', 1001)

    Thread(target=server_comm_start).start()
    Thread(target=client_comm_start).start()
