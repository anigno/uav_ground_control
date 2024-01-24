import logging

from common.logging_provider import logging_initiator_by_code, logging_initiator_base

if __name__ == '__main__':
    logging_initiator_by_code.LoggingInitiatorByCode(log_files_path="d:/dev/logs/log")
    logger = logging.getLogger(logging_initiator_base.LoggingInitiatorBase.STREAM_LOGGER)
    logger.debug('started')
