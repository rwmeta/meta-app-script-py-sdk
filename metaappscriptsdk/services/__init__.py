# coding=utf-8
from metaappscriptsdk.exceptions import AuthError


def get_api_call_headers(app):
    """
    Генерирует заголовки для API запроса.
    Тут же подкладывается авторизация

    :type app: metaappscriptsdk.MetaApp
    """
    headers = {
        "content-type": "application/json;charset=UTF-8",
        "User-Agent": app.user_agent,
    }
    headers.update(app.developer_settings['api_headers'])
    return headers


def process_meta_api_error_code(status_code, request):
    if status_code == 401:
        raise AuthError(request)
