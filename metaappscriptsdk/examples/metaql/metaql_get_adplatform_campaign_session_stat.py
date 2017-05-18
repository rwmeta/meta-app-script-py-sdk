import os

from metaappscriptsdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

q = """
SELECT
  campaign_name,
  client_id,
  engine,
  SUM(users) as users
FROM adplatform.campaign_sessions_stats_report
WHERE stat_date BETWEEN '2017-03-01' AND '2017-03-31'
AND system = 'googleAnalytics'
GROUP BY campaign_name, client_id, engine
ORDER BY campaign_name, client_id, engine
"""

configuration = {
    "download": {
        # "skipHeaders": True,
        "dbQuery": {
            "command": q
        }
    }
}
META.auth_user_id = 10191
metaql = META.MetaqlService
resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/campaign_sessions_stats_report.tsv')
log.info("end")
