# coding=utf-8

import logging

from fluent import handler

from metaappscriptsdk.logger.custom_fluent import FluentHandler

# http://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library
# Отключаем логи от бибилиотеки requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def create_logger(service_id=None, debug=True):
    if not service_id:
        service_id = 'unknown'
    # http://stackoverflow.com/questions/3220284/how-to-customize-the-time-format-for-python-logging
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', datefmt="%H:%M:%S",
                        level=logging.INFO)

    if not debug:
        custom_format = {
            'service_id': service_id,
            'host': '%(hostname)s',
            'where': '%(module)s.%(funcName)s',
            'type': '%(levelname)s',
            'stack_trace': '%(exc_text)s'
        }

        h = FluentHandler('es.metaappscript', host='code.harpoon.lan', port=8899, verbose=False)
        formatter = handler.FluentRecordFormatter(custom_format)
        h.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(h)
