# coding=utf-8
import json



class FeedService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}
        self.__data_get_cache = {}
        self.__data_get_flatten_cache = {}

    def datasource_fetch(self, datasource_id):
        """
        Получает DataResult фида
        :param datasource_id: uuid
        """
        response = self.__app.native_api_call('feed', 'datasource/' + datasource_id + '/fetch', {}, self.__options, False, None, False,
                                              http_method="GET")
        return json.loads(response.text)

    def datasource_process(self, datasource_id):
        """
        Запускает настроенные обработки в фиде
        :param datasource_id: uuid
        """

        # TODO без applicationId не выбираются поля сущностей. Подумать на сколько это НЕ нормально
        response = self.__app.native_api_call('feed', 'datasource/' + datasource_id + '/process?applicationId=1', {}, self.__options, False, None, False,
                                              http_method="POST")
        return json.loads(response.text)
