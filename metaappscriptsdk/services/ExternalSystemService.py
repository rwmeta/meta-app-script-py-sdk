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

    def get_access(self, ex_access_id):
        ex_access = self.__metadb.one(
            """
            SELECT token_info
                 , form_data 
              FROM meta.ex_access 
             WHERE id=:id::uuid
            """,
            {"id": ex_access_id}
        )

        ex_access['token_info']['accessToken'] = decode_jwt(ex_access['token_info'].get('accessToken'), self.__crypt_params['secureKey'])
        ex_access['token_info']['refreshToken'] = decode_jwt(ex_access['token_info'].get('refreshToken'), self.__crypt_params['secureKey'])

        return ex_access
