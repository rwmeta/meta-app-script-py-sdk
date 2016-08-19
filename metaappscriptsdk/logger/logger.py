# coding=utf-8
import logging

from metaappscriptsdk.logger import LOGGER_ENTITY


class Logger:
    """
    Прослойка для упрощения апи логгера
    """

    def set_entity(self, key, value):
        if value is None:
            self.remove_entity(key)
        else:
            LOGGER_ENTITY[key] = value

    def remove_entity(self, key):
        LOGGER_ENTITY.pop(key, None)

    def info(self, msg, context=None):
        if context is None:
            context = {}
        logging.info(msg, extra={'context': context})

    def warning(self, msg, context=None):
        if context is None:
            context = {}
        logging.warning(msg, extra={'context': context})

    def error(self, msg, context=None):
        if context is None:
            context = {}
        logging.error(msg, extra={'context': context})

    def critical(self, msg, context=None):
        if context is None:
            context = {}
        logging.critical(msg, extra={'context': context})

    def exception(self, msg, context=None):
        if context is None:
            context = {}
        logging.exception(msg, extra={'context': context})
