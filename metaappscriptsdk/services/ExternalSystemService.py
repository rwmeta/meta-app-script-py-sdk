from ..utils import decode_jwt

class ExternalSystemService:
    def __init__(self, app, default_headers):
        """
        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}
        self.__data_get_cache = {}
        self.__data_get_flatten_cache = {}
        self.__metadb = app.db("meta")
        self.__crypt_params = app.SettingsService.data_get("crypt_params")

    def get_ex_access(self, ex_access_id):
        return self.__metadb.one(
            """
            SELECT token_info
                 , form_data 
              FROM meta.ex_access 
             WHERE id=:id::uuid
            """,
            {"id": ex_access_id}
        )

    def get_token(self, conn_ex_access_id):
        """
        Возвращает токен для подключения
        :param conn_ex_access_id:
        :return:
        """
        return decode_jwt(self.get_ex_access(conn_ex_access_id)['token_info']['accessToken'], self.__crypt_params)