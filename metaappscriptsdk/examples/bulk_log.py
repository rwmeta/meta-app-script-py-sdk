# coding=utf-8
import time

from metaappscriptsdk import MetaApp

META = MetaApp()

# Станартный вариант
total = 125
bulk_log = META.bulk_log(u'Моя пачка', total, 1)

for idx in range(total):
    bulk_log.try_log_part()
    time.sleep(1)
bulk_log.finish()

# На частых но возможно долгих процессах
bulk_log = META.bulk_log(u'Моя пачка', total, 1)

for idx in range(total):
    bulk_log.try_log_part(with_start_message=False)
