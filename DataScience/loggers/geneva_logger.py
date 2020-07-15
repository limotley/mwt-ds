from fluent import asyncsender as sender
import json
import sys
import traceback

from loggers.logger_base import LoggerBase

class GenevaLogger(LoggerBase):

    def __init__(self, namespace, host, port, **global_vals):
        sender.setup(namespace, host=host, port=port)
        self.global_vals = global_vals

    def __log(self, level, msg, tag, **kwargs):
        try:
            print("creating base log")
            base_log = {'level': level, 'message': msg}
            print("creating log content")
            log_content = {**base_log, **kwargs, **self.global_vals}
            print("sending log")
            logger = sender.get_global_sender()
            if not logger.emit(tag, log_content):
                print("emit failed")
                print(logger.last_error)
                logger.clear_last_error()
        except Exception as e:
            print("Error while logging: {}".format(e))
        print("reached end log")

    def info(self, msg: str, tag='log', **kwargs):
        print("in info")
        self.__log('INFO', msg, tag, **kwargs)

    def warning(self, msg: str, tag='log', **kwargs):
        self.__log('WARNING', msg, tag, **kwargs)

    def error(self, msg: str, tag='exception', **kwargs):
        self.__log('ERROR', msg, tag, **kwargs)

    def exception(self, msg: str='', tag='exception', **kwargs):
        self.error(msg, tag, exception=traceback.format_exc(), **kwargs)

    def close(self):
        sender.get_global_sender().close()
