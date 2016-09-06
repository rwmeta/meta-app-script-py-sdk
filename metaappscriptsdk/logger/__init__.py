# coding=utf-8

from __future__ import print_function

import logging
import sys
import traceback

from metaappscriptsdk.logger.custom_fluent import FluentHandler, FluentRecordFormatter

# http://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library
# Отключаем логи от бибилиотеки requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOGGER_ENTITY = {}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_logger(service_id=None, debug=True):
    if not service_id:
        service_id = 'unknown'
    # http://stackoverflow.com/questions/3220284/how-to-customize-the-time-format-for-python-logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = StdoutFormatter('%(asctime)s:%(levelname)s: %(message)s %(context)s', datefmt="%H:%M:%S")
    ch.setFormatter(formatter)

    root_logger.addHandler(ch)

    if not debug:
        custom_format = {
            'srv': service_id,
            'host': '%(hostname)s',
            'type': '%(levelname)s',
            'stack_trace': '%(exc_text)s'
        }

        h = FluentHandler('es.metaappscript', host='code.harpoon.lan', port=8899, verbose=False)
        formatter = FluentRecordFormatter(custom_format)
        h.setFormatter(formatter)
        root_logger.addHandler(h)


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
