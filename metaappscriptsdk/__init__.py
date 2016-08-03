import starter_api as starter_api

from metaappscriptsdk.logger import create_logger


class MetaApp(object):
    debug = False
    starter_api_url = None

    starter = starter_api

    def __init__(self, debug=False, starter_api_url="http://s2.meta.vmc.loc:28341"):
        self.debug = debug
        self.starter_api_url = starter_api_url

        create_logger(self)
        starter_api.init(self.starter_api_url)
