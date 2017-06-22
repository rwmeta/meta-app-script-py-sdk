# coding=utf-8
import json


class ExportService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}

    def export_page(self, app_id, page_id, export_data_ids, params=None, export_format="csv"):
        if params is None:
            params = {"stateParams": {}}
        response = self.__app.native_api_call('export', 'page', params, self.__options, get_params={
            "applicationId": app_id,
            "entityPageId": page_id,
            "exportFormat": export_format,
            "exportDataIds": export_data_ids,
        })
        return json.loads(response.text)
