import logging.config
import json
import random
import time

from python.common.logging_provider.logging_initiator_base import LoggingInitiatorBase

class LoggingInitiatorWithConfig(LoggingInitiatorBase):

    def __init__(self, logging_config_file: str):
        super().__init__()
        logging.config.dictConfig(json.load(open(logging_config_file, 'r')))

if __name__ == '__main__':
    LoggingInitiatorWithConfig('logging_config.json')
    logger = logging.getLogger(LoggingInitiatorBase.FILE_SYSTEM_LOGGER)
    for i in range(400):
        level = random.randint(0, 5) * 10
        long_string = '123456789_' * 300
        logger.log(level=level, msg=f'{i} {long_string}')
        time.sleep(.1)
