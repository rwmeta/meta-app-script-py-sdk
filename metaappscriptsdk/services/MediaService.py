# coding=utf-8


class MediaService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}

    def persist_one(self, file_base64_content, filename, extension, mime, is_private=True):
        """
        Загружает файл в облако
        :type origin: string Принимает значения ROBOT, USER
        """
        return self.__app.api_call("MediaService", "persist_one", locals(), {})

    def download(self, media_id, as_stream=False):
        """
        Скачивает указанный файл
        :param media_id: string
        :rtype: requests.Response
        """
        response = self.__app.native_api_call('media', 'd/' + media_id, {}, self.__options, False, None, as_stream, http_path="/", http_method='GET')
        return response
