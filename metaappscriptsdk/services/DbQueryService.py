# coding=utf-8
import json

from metaappscriptsdk.services import api_call


class DbQueryService:
    def __init__(self, app, default_headers, options):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = options

    def update(self, command, params=None, shard_id=None):
        return api_call("DbQueryService", "update", locals(), self.__options, self.__app, self.__default_headers)

    def query(self, command, params=None, shard_id=None):
        """
        Выполняет запрос, который ОБЯЗАТЕЛЬНО должен вернуть результат.
        Если вам надо сделать INSERT, UPDATE, DELETE или пр. используйте метод update
        или возвращайте результата через конструкцию RETURNING (нет в MySQL)

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :rtype: object DataResult
        :param command: SQL запрос
        :param params: Параметры для prepared statements
        :param shard_id: ID шарды для шардируемых БД
        """
        return api_call("DbQueryService", "query", locals(), self.__options, self.__app, self.__default_headers)


    def one(self, command, params=None, shard_id=None):
        """
        Выполняет запрос, который ОБЯЗАТЕЛЬНО должен вернуть результат.
        Если вам надо сделать INSERT, UPDATE, DELETE или пр. используйте метод update
        или возвращайте результата через конструкцию RETURNING (нет в MySQL)

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :rtype: object DataResult
        :param command: SQL запрос
        :param params: Параметры для prepared statements
        :param shard_id: ID шарды для шардируемых БД
        """
        dr = self.query(command, params, shard_id)
        return dr['rows'][0]
