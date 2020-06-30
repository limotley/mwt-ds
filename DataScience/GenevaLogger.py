from fluent import asyncsender as sender
import json
import sys

class Logger:
    app_id = ""
    job_id = ""

    @staticmethod
    def create_logger(app_id, job_id):
        sender.setup('microsoft.cloudai.personalization', host='localhost', port=24224)
        Logger.app_id = app_id
        Logger.job_id = job_id

    @staticmethod
    def __log(level, msg, output=sys.stdout, tag='log', **kwargs):
        try:
            print("printing", flush=True)
            print(msg, file=output, flush=True)
            print("done printing", flush=True)
            base_log = {'level': level, 'message': msg, 'appId': Logger.app_id, 'jobId': Logger.job_id}
            log_content = {**base_log, **kwargs}
            print("logging", flush=True)
            print(log_content)
            logger = sender.get_global_sender()
            if not logger.emit(tag, log_content):
                print(logger.last_error)
                logger.clear_last_error()
            else:
                print("logging done", flush=True)
        except Exception as e:
            print("Error while logging: {}".format(e), flush=True)

    @staticmethod
    def info(msg: str):
        Logger.__log('INFO', msg)

    @staticmethod
    def warning(msg: str):
        Logger.__log('WARNING', msg)

    @staticmethod
    def error(msg: str, **kwargs):
        Logger.__log('ERROR', msg, sys.stderr, 'exception', **kwargs)

    @staticmethod
    def exception(e_type, e_value, e_traceback, msg: str=None):
        Logger.error(msg, exceptionType=e_type, exceptionValue=e_value, exceptionTraceback=e_traceback)

    @staticmethod
    def close():
        logger = sender.get_global_sender()
        logger.close()