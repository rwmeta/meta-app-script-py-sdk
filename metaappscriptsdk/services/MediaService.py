import json

import requests

from metaappscriptsdk.services import process_meta_api_error_code


class MediaService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers

    def persist_one(self, file_base64_content, filename, extension, mime, is_private, origin):
        data = locals()
        data.pop("self")
        body = json.dumps(data)
        host = self.__app.meta_url
        request = {
            "url": host + "/api/v1/adptools/media/persist_one",
            "data": body,
            "headers": self.__default_headers
        }
        resp = requests.post(**request)
        if resp.status_code == 200:
            return json.loads(resp.text)['data']['persist_one']
        else:
            process_meta_api_error_code(resp.status_code, request)
