# coding=utf-8

from __future__ import print_function
import atexit
import logging
import sys
import traceback
import socket

from logstash import formatter as logstash_formatter
from logging.handlers import SocketHandler
from logstash import formatter
from fluent import handler
import metaappscriptsdk

# http://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library
# Отключаем логи от бибилиотеки requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOGGER_ENTITY = {}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_logger(service_id=None, service_ns=None, build_num=None, debug=True):
    if not service_id:
        service_id = 'unknown'
    if not build_num:
        build_num = 0
    # http://stackoverflow.com/questions/3220284/how-to-customize-the-time-format-for-python-logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = StdoutFormatter('%(asctime)s:%(levelname)s: %(message)s %(context)s', datefmt="%H:%M:%S")
    ch.setFormatter(formatter)

    root_logger.addHandler(ch)

    if not debug:
        h = handler.FluentHandler(service_ns + '.' + service_id, host='n3.adp.vmc.loc', port=31891)
        h.setFormatter(GCloudFormatter())
        root_logger.addHandler(h)

        def exit_handler():
            # Обязательно закрыть сокет по доке
            # https://github.com/fluent/fluent-logger-python
            h.close()

        atexit.register(exit_handler)

    if not debug:
        h = TCPLogstashHandler(host='192.168.3.27', port=24224)
        h.setFormatter(LogstashFormatter(message_type="logstash", tags=None, fqdn=True, service_id=service_id, build_num=build_num, debug=debug))
        root_logger.addHandler(h)


class GCloudFormatter(handler.FluentRecordFormatter, object):
    def format(self, record):
        # Create message dict
        context = record.context if hasattr(record, 'context') else {}
        context.update(metaappscriptsdk.logger.LOGGER_ENTITY)

        if record.exc_info:
            context.update(self.formatException(record))

        message = {
            "message": record.getMessage(),
            "context": context,
            "severity": record.levelname
        }
        return message

    def formatException(self, record):
        """
        Format and return the specified exception information as a string.
        :type record logging.LogRecord
        :rtype: dict
        """
        if record.exc_info is None:
            return {}

        (exc_type, exc_message, trace) = record.exc_info

        return {
            'e': {
                'class': str(exc_type.__name__),  # ZeroDivisionError
                'message': str(exc_message),  # integer division or modulo by zero
                'trace': list(traceback.format_tb(trace)),
            }
        }


class StdoutFormatter(logging.Formatter, object):
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        dict__ = record.__dict__
        dict__.setdefault('context', {})
        context = dict__.get('context')
        context.update(LOGGER_ENTITY)
        ex = context.get("e")
        if ex:
            context.update({'e': {
                'class': str(ex.__class__),
                'message': str(ex),
                'trace': str(traceback.format_exc()),
            }})
            eprint(str(ex) + "\n" + str(traceback.format_exc()))
        s = self._fmt % dict__
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')
        return s


class TCPLogstashHandler(SocketHandler, object):
    """Python logging handler for Logstash. Sends events over TCP.
    :param host: The host of the logstash server.
    :param port: The port of the logstash server (default 5959).
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(self, host, port=5959, message_type='logstash', tags=None, fqdn=False, version=0):
        super(TCPLogstashHandler, self).__init__(host, port)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, tags, fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, tags, fqdn)

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'

    def makeSocket(self, timeout=10):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        if self.port is not None:
            result = socket.create_connection(self.address, timeout=timeout)
        else:
            result = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            result.settimeout(timeout)
            try:
                result.connect(self.address)
            except OSError:
                result.close()
                raise
        return result


class LogstashFormatter(logstash_formatter.LogstashFormatterBase):
    def __init__(self, message_type='logstash', tags=None, fqdn=False, service_id='unknown', build_num=0, debug=False):
        super().__init__(message_type, tags, fqdn)
        self.service_id = service_id
        self.build_num = build_num
        self.debug = debug

    def format(self, record):
        # Create message dict
        context = record.context if hasattr(record, 'context') else {}
        context.update(metaappscriptsdk.logger.LOGGER_ENTITY)
        context.setdefault('srv', self.service_id)
        context.setdefault('bnum', self.build_num)

        if record.exc_info:
            context.update(self.format_exception(record))

        message = {
            "message": record.getMessage(),
            "context": context,
            "level": record.levelno,
            "level_name": record.levelname,
            "channel": "es.metaappscript",
            "extra": {}
        }

        return self.serialize(message)

    def formatException(self, record):
        """
        Format and return the specified exception information as a string.
        :type record logging.LogRecord
        :rtype: dict
        """
        if record.exc_info is None:
            return {}

        (exc_type, exc_message, trace) = record.exc_info

        return {
            'e': {
                'class': str(exc_type.__name__),  # ZeroDivisionError
                'message': str(exc_message),  # integer division or modulo by zero
                'trace': list(traceback.format_tb(trace)),
            }
        }
