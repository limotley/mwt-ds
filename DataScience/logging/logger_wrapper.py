from fluent import asyncsender as sender
import json
import sys
import traceback
from logging.geneva_logger import GenevaLogger 
from logging.console_logger import ConsoleLogger

class Logger:
    loggers = []

    @staticmethod
    def create_loggers(geneva=False, **geneva_args):
        Logger.loggers.append(ConsoleLogger())
        if geneva:
            Logger.loggers.append(GenevaLogger(**geneva_args))

    @staticmethod
    def info(msg: str, **kwargs):
        for logger in Logger.loggers:
            logger.info(msg, **kwargs)

    @staticmethod
    def warning(msg: str, **kwargs):
        for logger in Logger.loggers:
            logger.warning(msg, **kwargs)

    @staticmethod
    def error(msg: str, **kwargs):
        for logger in Logger.loggers:
            logger.error(msg, **kwargs)

    @staticmethod
    def exception(msg: str='', **kwargs):
        for logger in Logger.loggers:
            logger.exception(msg, **kwargs)

    @staticmethod
    def close():
        for logger in Logger.loggers:
            logger.close()
