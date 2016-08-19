# coding=utf-8
import os

import starter_api as starter_api
import sys

from metaappscriptsdk.logger import create_logger
from metaappscriptsdk.logger.bulk_logger import BulkLogger
from metaappscriptsdk.logger.logger import Logger
from metaappscriptsdk.starter.worker import Worker


class MetaApp(object):
    debug = False
    service_id = None
    starter_api_url = None
    starter = starter_api
    log = Logger()
    worker = None

    def __init__(self, service_id=None, debug=None, starter_api_url="http://localhost/mystarter"):
        if not debug:
            debug = os.environ.get('DEBUG', True)
            if debug == 'false':
                debug = False
        self.debug = debug

        deprecated_logs = []

        if service_id:
            deprecated_logs.append(u"Параметр service_id скоро будет удален из MetaApp")

        service_id = os.environ.get('SERVICE_ID', "local_debug_serivce")
        self.service_id = service_id
        create_logger(service_id=service_id, debug=self.debug)

        for deprecated_log_msg in deprecated_logs:
            self.log.warning("#" * 15)
            self.log.warning("#" * 15)
            self.log.warning("# " + deprecated_log_msg)
            self.log.warning("#" * 15)
            self.log.warning("#" * 15)

        self.log.info(u'Инициализация службы', {"debug": debug})

        if not debug:
            starter_api_url = "http://s2.meta.vmc.loc:28341"
        self.starter_api_url = starter_api_url
        starter_api.init(self.starter_api_url)

        if sys.stdin.isatty():
            print("Waiting stdin...")
            stdin = ''.join(sys.stdin.readlines())
        else:
            print("Empty stdin...")
            stdin = "[]"

        self.worker = Worker(self, stdin)

    def bulk_log(self, log_message=u"Еще одна пачка обработана", total=None, part_log_time_minutes=5):
        """
        Возвращает инстант логгера для обработки списокв данных
        :param log_message: То, что будет написано, когда время придет
        :param total: Общее кол-во объектов, если вы знаете его
        :param part_log_time_minutes: Раз в какое кол-во минут пытаться писать лог
        :return: BulkLogger
        """
        return BulkLogger(log=self.log, log_message=log_message, total=total, part_log_time_minutes=part_log_time_minutes)
