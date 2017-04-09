# coding=utf-8
import json

import shutil


class MetaqlService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}

    def download_data(self, configuration, output_file):
        params = configuration
        response = self.__app.native_api_call('metaql', 'download-data', params, self.__options, False, None, True, http_path="/api/v1/meta/")
        with open(output_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
