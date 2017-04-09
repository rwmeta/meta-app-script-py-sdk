import os

from metaappscriptsdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": """
            SELECT organization_id, SUM(salary) as sum_salary
            FROM meta_samples.employee
            GROUP BY organization_id
            ORDER BY sum_salary DESC
            """
        }
    }
}

metaql = META.MetaqlService
resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/out_employee.tsv')
