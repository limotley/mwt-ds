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
    def __log(level, msg, output=sys.stdout, tag='log'):
        try:
            print("print")
            print(msg, file=output, flush=True)
            print("done print")
            base_log = {'level': level, 'message': str(msg), 'appId': Logger.app_id, 'jobId': Logger.job_id}
            logger = sender.get_global_sender()
            logger.emit(tag, base_log)
        except Exception as e:
            print("Error while logging: {}".format(e), flush=True)

    @staticmethod
    def info(msg):
        Logger.__log('INFO', msg)

    @staticmethod
    def warning(msg):
        Logger.__log('WARNING', msg)

    @staticmethod
    def error(msg):
        Logger.__log('ERROR', msg, sys.stderr, 'exception')

    @staticmethod
    def close():
        logger = sender.get_global_sender()
        logger.close()