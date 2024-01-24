import logging
import logging.config
import pickle
import socket
import sys

from common.logging_provider.logging_initiator_base import LoggingInitiatorBase
from common.logging_provider.logging_initiator_with_config import LoggingInitiatorWithConfig

class DatagramLogReceiver:
    def __init__(self, datagram_endpoint: tuple[str, int]):
        LoggingInitiatorWithConfig('file_system_logging_config.json')
        logger = logging.getLogger(LoggingInitiatorBase.FILE_SYSTEM_LOGGER)
        logger.info(f'datagram logging service waiting on: {datagram_endpoint}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(datagram_endpoint)
        sys.stderr.write(f'*********************************\n'
                         f'* Starting datagram log service *\n'
                         f'* {datagram_endpoint} \n'
                         f'*********************************\n')
        while True:
            data, addr = sock.recvfrom(65535)
            log_record_object = pickle.loads(data[4:])  # first 4 bytes are the length of the pickled object
            log_record = logging.makeLogRecord(log_record_object)
            logger.handle(log_record)

if __name__ == '__main__':
    DatagramLogReceiver(('localhost', 9999))
