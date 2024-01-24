import logging
import sys
import random
import time

from common.logging_provider.logging_initiator_base import LoggingInitiatorBase
from common.logging_provider.reverse_rotating_file_handler import ReverseRotatingFileHandler

class LoggingInitiatorByCode(LoggingInitiatorBase):

    def __init__(self, log_files_path: str = "d:/dev/logs/log", backup_files_count: int = 1000,
                 datagram_endpoint: tuple[str, int] = ('localhost', 9999)):
        super().__init__()
        log_viewer_formatter = logging.Formatter(
            "$%(asctime)s|%(threadName)s|%(levelname)s|%(module)s,%(funcName)s|%(message)s")

        file_system_handler = ReverseRotatingFileHandler(prefix="log.txt", path=log_files_path, mode="a",
                                                         max_bytes=2_097_152,
                                                         backup_count=backup_files_count, delay=False)
        file_system_handler.formatter = log_viewer_formatter
        file_system_handler.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(stream=sys.stdout)
        # for ensuring output stderr could be used instead
        # stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.formatter = log_viewer_formatter
        stream_handler.setLevel(logging.DEBUG)

        datagram_handler = logging.handlers.DatagramHandler(datagram_endpoint[0], datagram_endpoint[1])
        datagram_handler.formatter = log_viewer_formatter
        datagram_handler.setLevel(logging.DEBUG)

        file_system_logger = logging.getLogger(LoggingInitiatorByCode.FILE_SYSTEM_LOGGER)
        file_system_logger.setLevel(logging.DEBUG)
        file_system_logger.addHandler(file_system_handler)
        file_system_logger.addHandler(stream_handler)

        stream_only_logger = logging.getLogger(LoggingInitiatorByCode.STREAM_LOGGER)
        stream_only_logger.setLevel(logging.DEBUG)
        stream_only_logger.addHandler(stream_handler)

        datagram_logger = logging.getLogger(LoggingInitiatorByCode.DATAGRAM_LOGGER)
        datagram_logger.setLevel(logging.DEBUG)
        datagram_logger.addHandler(datagram_handler)
        datagram_logger.addHandler(stream_handler)

if __name__ == '__main__':
    LoggingInitiatorByCode(log_files_path="d:/dev/logs/log", backup_files_count=1000,
                           datagram_endpoint=('localhost', 9999))
    logger = logging.getLogger(LoggingInitiatorBase.DATAGRAM_LOGGER)
    for i in range(400):
        level = random.randint(0, 5) * 10
        long_string = '123456789_' * 300
        logger.log(level=level, msg=f'{i} {long_string}')
        time.sleep(.01)
