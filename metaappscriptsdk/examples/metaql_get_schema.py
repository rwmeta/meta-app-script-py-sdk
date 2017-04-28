import os

from metaappscriptsdk import MetaApp, pretty_json

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

metaql = META.MetaqlService
resp = metaql.get_schema("adplatform", "campaign_stats_report")
print("Schema:\n")
print(pretty_json(resp))
log.info("end")
