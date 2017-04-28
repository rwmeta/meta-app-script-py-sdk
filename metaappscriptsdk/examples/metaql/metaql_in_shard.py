# coding=utf-8
import os

from metaappscriptsdk import MetaApp

META = MetaApp()
# META = MetaApp(meta_url="http://localhost:8080")
log = META.log

account_id = 137506

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": """
            SELECT match_type, count(id) as cnt
            FROM garpun_storage.keyword#{account_id}
            group by match_type
            """.format(account_id=account_id)
        }
    }
}

print(u"configuration = %s" % str(configuration))
metaql = META.MetaqlService

log.info("Save Start")

resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/out_keyword3.tsv')
print(u"resp.status_code = %s" % str(resp))

log.info("Save Done")
