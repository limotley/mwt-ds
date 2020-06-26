from fluent import asyncsender as sender
import json


class GenevaLogger(object):
    __logger = None

    def __init__(self, app_id, job_id):
        self.__logger = sender.FluentSender(
            'microsoft.cloudai.personalization', host='localhost', port=24224)
        self.app_id = app_id
        self.job_id = job_id

    def info(self, msg, *args, **kwargs):
        print(msg)
        base_log = {'level': 'INFO', 'message': msg, 'app_id': self.app_id, 'job_id': self.job_id}
        log_content = {**base_log, **kwargs}
        self.__logger.emit('log', log_content)

    def warning(self, msg, *args, **kwargs):
        print(msg)
        base_log = {'level': 'WARNING', 'message': msg, 'app_id': self.app_id, 'job_id': self.job_id}
        log_content = {**base_log, **kwargs}
        self.__logger.emit('log', log_content)

    def error(self, msg, *args, **kwargs):
        print(msg)
        base_log = {'level': 'ERROR', 'message': msg, 'app_id': self.app_id, 'job_id': self.job_id}
        log_content = {**base_log, **kwargs}
        self.__logger.emit('log', log_content)

    def track_exception(self, v_type, value, traceback, properties):
        base_log = {'level': 'EXCEPTION', 'type': v_type,
                             'value': value, 'traceback': traceback, 
                             'app_id': self.app_id, 'job_id': self.job_id}
        log_content = {**base_log, **properties}
        self.__logger.emit('log', log_content)
