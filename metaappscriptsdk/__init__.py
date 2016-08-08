import starter_api as starter_api

from metaappscriptsdk.logger import create_logger
from metaappscriptsdk.logger.logger import Logger


class MetaApp(object):
    debug = False
    starter_api_url = None
    starter = starter_api
    log = Logger()

    def __init__(self, service_id=None, debug=False, starter_api_url="http://s2.meta.vmc.loc:28341"):
        self.debug = debug
        self.starter_api_url = starter_api_url

        create_logger(service_id=service_id, debug=self.debug)
        starter_api.init(self.starter_api_url)
