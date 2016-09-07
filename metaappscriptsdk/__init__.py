# coding=utf-8
import json
import os
import sys
from os.path import expanduser

import starter_api as starter_api

from metaappscriptsdk.logger import create_logger
from metaappscriptsdk.logger.bulk_logger import BulkLogger
from metaappscriptsdk.logger.logger import Logger
from metaappscriptsdk.services import get_api_call_headers
from metaappscriptsdk.services.DbQueryService import DbQueryService
from metaappscriptsdk.services.MediaService import MediaService
from metaappscriptsdk.worker import Worker


class MetaApp(object):
    debug = False
    service_id = None
    starter_api_url = None
    meta_url = None
    starter = starter_api
    log = Logger()
    worker = None
    user_agent = None
    developer_settings = None

    # Пользователь, из под которого пройдет авторизация после того,
    # как мета авторизует разработчика, в случае, если разработчик имеет разрешения для авторизации из-под других пользователей
    auth_user_id = None

    MediaService = None

    __default_headers = set()
    __db_list = {}

    def __init__(self, service_id=None, debug=None,
                 starter_api_url="http://STUB_URL",
                 meta_url="http://meta.realweb.ru",
                 include_worker=None
                 ):
        if debug is None:
            debug = os.environ.get('DEBUG', True)
            include_worker = True
            if debug == 'false':
                debug = False
        self.debug = debug

        deprecated_logs = []

        if service_id:
            deprecated_logs.append(u"Параметр service_id скоро будет удален из MetaApp")

        service_id = os.environ.get('SERVICE_ID', "local_debug_serivce")
        self.service_id = service_id
        create_logger(service_id=service_id, debug=self.debug)

        self.__read_developer_settings()
        self.user_agent = self.__build_user_agent()

        for deprecated_log_msg in deprecated_logs:
            self.log.warning("#" * 15)
            self.log.warning("#" * 15)
            self.log.warning("# " + deprecated_log_msg)
            self.log.warning("#" * 15)
            self.log.warning("#" * 15)

        self.log.info(u'Инициализация службы', {"debug": debug})

        if not debug:
            starter_api_url = "http://s2.meta.vmc.loc:28341"
            meta_url = "http://meta.realweb.ru"

        self.meta_url = meta_url
        self.starter_api_url = starter_api_url
        starter_api.init(self.starter_api_url)

        self.__default_headers = get_api_call_headers(self)
        self.MediaService = MediaService(self, self.__default_headers)

        if include_worker:
            if not debug:
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

    def db(self, db_alias, shard_find_key=None):
        """
        Получить экземпляр работы с БД
        :type db_alias: basestring Альяс БД из меты
        :type shard_find_key: Любой тип. Некоторый идентификатор, который поможет мете найти нужную шарду. Тип зависи от принимающей стороны
        :rtype: DbQueryService
        """
        if shard_find_key is None:
            shard_find_key = ''

        db_key = db_alias + '__' + str(shard_find_key)
        if db_key not in self.__db_list:
            self.__db_list[db_key] = DbQueryService(self, self.__default_headers, {"db_alias": db_alias, "shard_find_key": shard_find_key})
        return self.__db_list[db_key]

    def __build_user_agent(self):
        v = sys.version_info
        return self.service_id + " | Python " + str(v.major) + "." + str(v.minor) + "." + str(v.micro) + " SDK os:" + os.name

    def __read_developer_settings(self):
        """
        Читает конфигурации разработчика с локальной машины или из переменных окружения
        При этом переменная окружения приоритетнее
        :return:
        """
        dev_key_path = "/.rwmeta/developer_settings.json"
        is_windows = os.name == "nt"
        if is_windows:
            dev_key_path = dev_key_path.replace("/", "\\")
        dev_key_full_path = expanduser("~") + dev_key_path
        if os.path.isfile(dev_key_full_path):
            self.log.info(u"Читаем настройки разработчика из локального файла", {"path": dev_key_full_path})
            with open(dev_key_full_path, 'r') as myfile:
                self.developer_settings = json.loads(myfile.read())

        env_developer_settings = os.environ.get('X-META-Developer-Settings', None)
        if env_developer_settings:
            self.log.info(u"Читаем настройки разработчика из переменной окружения")
            self.developer_settings = json.loads(env_developer_settings)

        if not self.developer_settings:
            self.log.warning(u"НЕ УСТАНОВЛЕНЫ настройки разработчика, это может приводить к проблемам в дальнейшей работе!")


def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
