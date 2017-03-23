# coding=utf-8
import json

import shutil


class DbQueryService:
    def __init__(self, app, default_headers, options):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = options

    def update(self, command, params=None):
        return self.__app.api_call("DbQueryService", "update", locals(), self.__options)

    def batch_update(self, command, params=None):
        return self.__app.api_call("DbQueryService", "batch_update", locals(), self.__options)

    def query(self, command, params=None):
        """
        Выполняет запрос, который ОБЯЗАТЕЛЬНО должен вернуть результат.
        Если вам надо сделать INSERT, UPDATE, DELETE или пр. используйте метод update
        или возвращайте результата через конструкцию RETURNING (нет в MySQL)

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :rtype: object DataResult
        :param command: SQL запрос
        :param params: Параметры для prepared statements
        """
        return self.__app.api_call("DbQueryService", "query", locals(), self.__options)

    def one(self, command, params=None):
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

    def all(self, command, params=None):
        """
        Возвращает строки ответа, полученного через query

        > db.query('SELECT * FORM users WHERE id=:id', {"id":MY_USER_ID})

        :param command: SQL запрос
        :param params: Параметры для prepared statements
        :rtype: list of dict
        """
        dr = self.query(command, params)
        return dr['rows']

    def schema_data(self, configuration):
        params = {"configuration": json.dumps(configuration)}
        dr = self.__app.native_api_call('db', 'schema-data', params, self.__options, True)
        return json.loads(dr.text)

    def upload_data(self, file_descriptor, configuration):
        multipart_form_data = {
            'file': file_descriptor
        }
        params = {"configuration": json.dumps(configuration)}
        dr = self.__app.native_api_call('db', 'upload-data', params, self.__options, True, multipart_form_data)
        return json.loads(dr.text)

    def download_data(self, configuration, output_file):
        params = {"configuration": json.dumps(configuration)}
        response = self.__app.native_api_call('db', 'download-data', params, self.__options, True, None, True)
        with open(output_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
