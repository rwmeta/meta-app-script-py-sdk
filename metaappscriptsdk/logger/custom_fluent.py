from fluent import handler, sender
import json


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
