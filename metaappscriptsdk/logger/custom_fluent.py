import hashlib
import json
import sys
import time
import traceback

import six
from fluent import handler, sender
from fluent.handler import FluentRecordFormatter

import metaappscriptsdk


class FluentSender(sender.FluentSender):
    def _make_packet(self, label, timestamp, data):
        if label:
            tag = '.'.join((self.tag, label))
        else:
            tag = self.tag

        if 'channel' not in data:
            data['channel'] = tag

        data['level_name'] = data['type']
        del data['type']
        packet = {'tag': tag, 'ts': timestamp, 'data': json.dumps(data, separators=(',', ':'))}

        message = ('["%(tag)s",%(ts)s,%(data)s]' % packet).encode('utf-8')
        if self.verbose:
            print(message)
        return message


class FluentHandler(handler.FluentHandler):
    def __init__(self, tag, host='localhost', port=24224, timeout=3.0, verbose=False):
        super(FluentHandler, self).__init__(tag, host=host, port=port, timeout=timeout, verbose=verbose)
        self.sender = FluentSender(tag, host=host, port=port, timeout=timeout, verbose=verbose)


class FluentRecordFormatter(FluentRecordFormatter, object):
    converter = time.gmtime  # timestamps are in UTC zone

    def formatTime(self, record, datefmt=None):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#mapping-date-format
        yyyy-MM-dd'T'HH:mm:ss.SSS # date_hour_minute_second_millis
        :type record logging.LogRecord
        :type datefmt str
        :rtype: str
        """
        ct = self.converter(record.created)

        # @see https://docs.python.org/2/library/time.html#time.strftime
        t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
        s = "%s.%03d" % (t, record.msecs)
        return s

    def format(self, record):
        dict__ = record.__dict__
        context = dict(dict__.get('context', {}))
        context.update(metaappscriptsdk.logger.LOGGER_ENTITY)
        # add exception details (if any)
        context.update(self.formatException(record))

        # Only needed for python2.6
        if sys.version_info[0:2] <= (2, 6) and self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        # Compute attributes handled by parent class.
        super(FluentRecordFormatter, self).format(record)
        # Add ours
        record.hostname = self.hostname
        # Apply format
        data = dict([(key, value % dict__)
                     for key, value in self._fmt_dict.items()])
        data['context'] = context
        data['@timestamp'] = self.formatTime(record)
        data.setdefault('extra', {})
        data['extra']['md5Msg'] = hashlib.md5(record.msg.encode('utf-8')).hexdigest()
        self._structuring(data, record.msg)
        return data

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

    def usesTime(self):
        return any([value.find('%(asctime)') >= 0
                    for value in self._fmt_dict.values()])

    def _structuring(self, data, msg):
        """ Melds `msg` into `data`.

        :param data: dictionary to be sent to fluent server
        :param msg: :class:`LogRecord`'s message to add to `data`.
          `msg` can be a simple string for backward compatibility with
          :mod:`logging` framework, a JSON encoded string or a dictionary
          that will be merged into dictionary generated in :meth:`format.
        """
        if isinstance(msg, dict):
            self._add_dic(data, msg)
        elif isinstance(msg, six.string_types):
            try:
                self._add_dic(data, json.loads(str(msg)))
            except ValueError:
                self._add_dic(data, {'message': msg})
        else:
            self._add_dic(data, {'message': msg})

    @staticmethod
    def _add_dic(data, dic):
        for key, value in dic.items():
            if isinstance(key, six.string_types):
                data[str(key)] = value
