import os
from metaappscriptsdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": "SELECT * FROM products WHERE productname ilike '%Gula%' LIMIT 1000"
        }
    }
}

db = META.db("nw")
db.download_data(configuration, output_file=__DIR__ + 'assets/out_products.tsv')
