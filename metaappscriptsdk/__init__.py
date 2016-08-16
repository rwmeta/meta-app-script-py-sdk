# coding=utf-8
import starter_api as starter_api

from metaappscriptsdk.logger import create_logger
from metaappscriptsdk.logger.bulk_logger import BulkLogger
from metaappscriptsdk.logger.logger import Logger


class MetaApp(object):
    debug = False
    starter_api_url = None
    starter = starter_api
    log = Logger()

    def __init__(self, service_id=None, debug=False, starter_api_url="http://s2.meta.vmc.loc:28341"):
        self.debug = debug
        self.starter_api_url = starter_api_url

        create_logger(service_id=service_id, debug=self.debug)
        starter_api.init(self.starter_api_url)

    def bulk_log(self, log_message=u"Еще одна пачка обработана", total=None, part_log_time_minutes=5):
        """
        Возвращает инстант логгера для обработки списокв данных
        :param log_message: То, что будет написано, когда время придет
        :param total: Общее кол-во объектов, если вы знаете его
        :param part_log_time_minutes: Раз в какое кол-во минут пытаться писать лог
        :return: BulkLogger
        """
        return BulkLogger(log=self.log, log_message=log_message, total=total, part_log_time_minutes=part_log_time_minutes)
