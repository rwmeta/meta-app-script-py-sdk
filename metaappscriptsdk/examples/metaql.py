import os

from metaappscriptsdk import MetaApp

META = MetaApp(meta_url="https://meta.realweb.ru")
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": """
            SELECT COALESCE(NULLIF(organization_id, 2), 42) as org, SUM(salary) as sum_salary
            FROM meta_samples.employee
            GROUP BY org
            ORDER BY sum_salary DESC
            """
        }
    }
}

metaql = META.MetaqlService
resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/out_employee.tsv')
