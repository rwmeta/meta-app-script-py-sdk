# coding=utf-8

from typing import Dict, List

from metaappscriptsdk.services import api_call


class DbQueryService:
    def __init__(self, app, default_headers, options):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = options

    def update(self, command: str, params: dict = None):
        return api_call("DbQueryService", "update", locals(), self.__options, self.__app, self.__default_headers)

    def batch_update(self, command: str, params: List[Dict]):
        return api_call("DbQueryService", "batch_update", locals(), self.__options, self.__app, self.__default_headers)

    def query(self, command: str, params: dict = None):
        """
        Выполняет запрос, который ОБЯЗАТЕЛЬНО должен вернуть результат.
        Если вам надо сделать INSERT, UPDATE, DELETE или пр. используйте метод update
        или возвращайте результата через конструкцию RETURNING (нет в MySQL)

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :rtype: object DataResult
        :param command: SQL запрос
        :param params: Параметры для prepared statements
        """
        return api_call("DbQueryService", "query", locals(), self.__options, self.__app, self.__default_headers)

    def one(self, command: str, params: dict = None) -> dict:
        """
        Возвращает первую строку ответа, полученного через query

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :param command: SQL запрос
        :param params: Параметры для prepared statements
        :rtype: dict
        """
        dr = self.query(command, params)
        if dr['rows']:
            return dr['rows'][0]
        else:
            return None

    def all(self, command: str, params: dict = None) -> List[Dict]:
        """
        Возвращает строки ответа, полученного через query

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :param command: SQL запрос
        :param params: Параметры для prepared statements
        :rtype: list of dict
        """
        dr = self.query(command, params)
        return dr['rows']
