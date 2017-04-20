# coding=utf-8
import os

from metaappscriptsdk import MetaApp

# META = MetaApp(meta_url="https://meta.realweb.ru")
META = MetaApp(meta_url="http://localhost:8080")
log = META.log

account_id = 137506

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": """
            SELECT id, remote_id, text, match_type
            FROM garpun_storage.keyword#{account_id}
            """.format(account_id=account_id)
        }
    }
}

print(u"configuration = %s" % str(configuration))
metaql = META.MetaqlService

log.info("Save Start")

resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/out_keyword.tsv')
print(u"resp.status_code = %s" % str(resp))

log.info("Save Done")
