import logging.config

from configs.logger_settings import LogConfig


def get_logger(logger: str = 'console'):
    logging.config.dictConfig(LogConfig)
    return logging.getLogger(logger)
