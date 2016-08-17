from metaappscriptsdk import MetaApp
import logging

META = MetaApp(service_id="UnitTestService", debug=False)
log = META.log

log.set_entity('campaign_id', -1)
log.set_entity('test', True)
log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})
log.info('Info log')
log.error('Info log')

logging.info('Default logging')

log.remove_entity('test')
log.info('Info log2')
