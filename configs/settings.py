import logging.config

from pydantic import BaseModel


class AppSettings(BaseModel):
    name: str = 'FastapiTester'
    version: str = '0.1.0'
    DEBUG: bool = True


def get_logger(logger: str = 'console'):
    from configs.logger_settings import LogConfig

    logging.config.dictConfig(LogConfig)
    return logging.getLogger(logger)
