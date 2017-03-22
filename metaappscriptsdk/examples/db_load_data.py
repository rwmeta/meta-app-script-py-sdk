import os

from metaappscriptsdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

upload_file = open(__DIR__ + 'assets/load_data_sample.tsv', 'rb')


configuration = {
    "load": {
        "destinationTable": {
            "schema": "public",
            "table": "xxx_ya_stat"
        },
        "schema": {
            "fields": [
                {"name": "Date", "type": "DATE"},
                {"name": "Clicks", "type": "LONG"},
                {"name": "Cost", "type": "DECIMAL"},
                {"name": "AdNetworkType", "type": "TEXT"},
            ]
        }
    }
}

db = META.db("meta_samples")
db.load_data(upload_file, configuration)
