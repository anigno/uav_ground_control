from abc import ABC
import logging

class LoggingInitiatorBase(ABC):
    STREAM_LOGGER = "stream_only_logger"
    FILE_SYSTEM_LOGGER = "file_system_logger"
    DATAGRAM_LOGGER = 'datagram_logger'
    MESSAGE_ONLY_LOGGER = 'message_only_logger'

    def __init__(self):
        logging.addLevelName(logging.WARNING, "WARN")
        logging.addLevelName(logging.CRITICAL, "FATAL")
