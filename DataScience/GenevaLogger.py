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
    def __log(level, msg, output=sys.stdout, *args, **kwargs):
        print(msg, file=output)
        output.flush()
        base_log = {'level': level, 'message': msg, 'appId': Logger.app_id, 'jobId': Logger.job_id}
        log_content = {**base_log, **kwargs}
        logger = sender.get_global_sender()
        logger.emit('log', log_content)

    @staticmethod
    def info(msg, *args, **kwargs):
        Logger.__log('INFO', msg)

    @staticmethod
    def warning(msg, *args, **kwargs):
        Logger.__log('WARNING', msg)

    @staticmethod
    def error(msg, *args, **kwargs):
        Logger.__log('ERROR', msg, sys.stderr)

    @staticmethod
    def close():
        logger = sender.get_global_sender()
        logger.close()