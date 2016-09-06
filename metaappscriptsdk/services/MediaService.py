# coding=utf-8

from metaappscriptsdk.services import api_call


class MediaService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers

    def persist_one(self, file_base64_content, filename, extension, mime, is_private=True, origin="ROBOT"):
        """
        Загружает файл в облако
        :type origin: string Принимает значения ROBOT, USER
        """
        return api_call("MediaService", "persist_one", locals(), {}, self.__app, self.__default_headers)
