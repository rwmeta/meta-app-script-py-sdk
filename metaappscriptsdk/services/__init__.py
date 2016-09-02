# coding=utf-8
import json

import requests

from metaappscriptsdk.exceptions import AuthError, DbQueryError, UnexpectedResponseError
from metaappscriptsdk.logger import eprint


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
    if not app.developer_settings:
        raise AuthError({u"message": u"Для корректной работы SDK нужно установить настройки разработчика", "url": "http://meta.realweb.ru/page?a=63&p=3975"})
    headers.update(app.developer_settings.get('api_headers'))
    return headers


def process_meta_api_error_code(status_code, request):
    if status_code == 401:
        raise AuthError(request)


def api_call(service, method, data, options, app, default_headers):
    """
    :type app: metaappscriptsdk.MetaApp
    """
    data.pop("self")
    if options:
        data.update(options)

    request = {
        "url": app.meta_url + "/api/v1/adptools/" + service + "/" + method,
        "data": json.dumps(data),
        "headers": default_headers
    }
    resp = requests.post(**request)
    if resp.status_code == 200:
        decoded_resp = json.loads(resp.text)
        if 'data' in decoded_resp:
            return decoded_resp['data'][method]
        if 'error' in decoded_resp:
            if 'details' in decoded_resp['error']:
                eprint(decoded_resp['error']['details'])
            raise DbQueryError(decoded_resp['error'])
        raise UnexpectedResponseError()
    else:
        process_meta_api_error_code(resp.status_code, request)
