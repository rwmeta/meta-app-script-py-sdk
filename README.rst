=========================
Meta App Script SDK
=========================


Install
=======
pip install metaappscriptsdk

Последний резил для Python 2 = 0.1.3
Python 3 начинается с > 0.3.0

Full Examples
=============

`Полный список примеров
<https://github.com/rw-meta/meta-app-script-py-sdk/tree/master/metaappscriptsdk/examples/>`_

Usage
=====
.. code-block:: python

    # coding=utf-8
    import logging
    import starter_api
    from metaappscriptsdk import MetaApp

    # Инициализация приложения
    # конфигурирует логгер и пр.
    META = MetaApp()

    # работает стандартный логгер
    logging.info('Hello, from Meta App Script!')
    # Можно получить экземпляр логгера с улучшеным интерфейсом для более удобного прикладывания контекста
    log = META.log
    log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})

    # Поставновка задач в Запускатор
    starter_api.build_submit('YOUR_SERVICE')
    # или
    META.starter.build_submit('YOUR_SERVICE')


Logger
=====
.. code-block:: python

    log = META.log

    # Объявите глобальный контекст, чтобы не писать это каждый раз
    log.set_entity('campaign_id', -1)
    # По сути это просто хранилище глобавльных переменных контекста
    log.set_entity('test', True)
    log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})
    log.info('Info log')

    logging.info('Default logging')

    # удалите глобальный контекст, когда он вам больше не нужен
    log.remove_entity('test')
    log.info('Info log2')

Это выведет вам что-то вроде такого:

.. code-block:: python

    #  00:03:11:WARNING: Do warning log {'count': 1, 'mycontextParam': [1, 3, 4], 'test': True, 'campaign_id': -1}
    #  00:03:11:INFO: Info log {'test': True, 'campaign_id': -1}
    #  00:03:11:INFO: Default logging {'test': True, 'campaign_id': -1}
    #  00:03:11:INFO: Info log2 {'campaign_id': -1}



Bulk Logger
=====
Используется для логирования пачек из обрабатываемого списка.
Делает запись в лог только если прошло определенное кол-во времени

.. code-block:: python

    total = 125
    # Получаете инстанс bulk-логгера через объект приложения
    # Список параметров вам подскажет IDE
    bulk_log = META.bulk_log(u'Моя пачка', total, 1)

    for idx in xrange(total):
        # Первый вызов всегда try_log_part, чтобы ознаменовать начало выполнения цикла
        bulk_log.try_log_part()

        # На ЧАСТЫХ, но возможно БЫСТРЫХ процессах можете использовать параметр with_start_message=False
        # Это исключит запись надписи о начале работы над пачкой и, если пачка сделается до
        # мин. время логирования, то записи не произойдет вообще
        # bulk_log.try_log_part(with_start_message=False)

        # далее ваша бизнес-логика
        time.sleep(1)

    # finish вызывать необязательно, но часто нужно,
    # чтобы точно сказать, что обработка выполнена
    bulk_log.finish()

Это выведет вам что-то вроде такого:

.. code-block:: python

    # 23:55:31:INFO: Начали цикл: Моя пачка {}
    # 23:56:31:INFO: Моя пачка {'counter': 61, 'percentDone': 48, 'maxCount': 125}
    # 23:57:31:INFO: Моя пачка {'counter': 121, 'percentDone': 96, 'maxCount': 125}
    # 23:57:36:INFO: Закончили цикл: Моя пачка {}



Bulk Logger Thread Pool
=====
Используется для логирования пачек из обрабатываемого списка.
Делает запись в лог только если прошло определенное кол-во времени

.. code-block:: python

    # coding=utf-8
    import time
    from functools import partial
    from multiprocessing.pool import ThreadPool

    from metaappscriptsdk import MetaApp

    META = MetaApp()


    def my_thread_fn(bulk_log, job_item):
        bulk_log.try_log_part()
        # Бизнес логика
        # работа с job_item
        time.sleep(1)


    def my_main_fn():
        total = 125 * 2
        thread_cnt = 2

        bulk_log = META.bulk_log(u'Моя пачка', total, 1)
        bulk_log.try_log_part()

        all_data = range(1, total)
        pool = ThreadPool(thread_cnt)

        # Чтобы работать в многопоточном режиме с bulk_log вы
        # должны передать его как аргумент вызываемой функции таким образом
        func = partial(my_thread_fn, bulk_log)
        results = pool.map(func, all_data)

        bulk_log.finish()
        pool.close()
        pool.join()
        #print(results)

    my_main_fn()


Это выведет вам что-то вроде такого:

.. code-block:: python

    # 16:25:08:INFO: Начали цикл: Моя пачка {}
    # 16:26:08:INFO: Моя пачка {'counter': 122, 'percentDone': 48, 'maxCount': 250}
    # 16:27:09:INFO: Моя пачка {'counter': 242, 'percentDone': 96, 'maxCount': 250}
    # 16:27:17:INFO: Закончили цикл: Моя пачка {}



RPC Meta Services
=====

MediaService
------------

.. code-block:: python

    # coding=utf-8
    import base64

    from metaappscriptsdk import MetaApp, pretty_json

    META = MetaApp()
    log = META.log

    # Получаете инстанс сервиса и делаете запрос к нему
    result = META.MediaService.persist_one(
        file_base64_content=base64.b64encode(b"Hello, from META!").decode("utf-8"),
        filename="req.txt",
        extension="txt",
        mime="plain/text",
        is_private=False,
        origin="ROBOT",
    )
    # Формат ответа стандартный для меты
    first = result['rows'][0]
    print(u"result['rows'][0]['url'] = %s" % first['url'])
    print(u"first = %s" % first)
    print(u"result = %s" % pretty_json(result))



Это выведет вам что-то вроде такого:

.. code-block:: python

    # 16:48:19:INFO: Читаем настройки разработчика из локального файла {'path': '/Users/arturgspb/.rwmeta/developer_settings.json'}
    # 16:48:19:INFO: Инициализация службы {'debug': True}
    # Empty stdin...
    # result['rows'][0]['url'] = http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b
    # first = {u'url': u'http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b', u'id': u'c6509ac7-b410-4f77-8f0b-7c1dfd6a871b', u'full_path': u'/mnt/static/public/74/reqtxt-2016-09-02_16-48-19-(4501).txt'}
    # result = {
    #     "boxed": false,
    #     "columns": [
    #         {
    #             "displayName": "Id",
    #             "fullDisplayName": "Id",
    #             "isPrimary": true,
    #             "isStyled": false,
    #             "name": "id",
    #             "role": "dimension",
    #             "type": "TEXT"
    #         },
    #         {
    #             "displayName": "url",
    #             "fullDisplayName": "url",
    #             "isStyled": true,
    #             "name": "url",
    #             "role": "dimension",
    #             "type": "TEXT"
    #         },
    #         {
    #             "displayName": "downloadUrlPart",
    #             "fullDisplayName": "downloadUrlPart",
    #             "isStyled": true,
    #             "name": "downloadUrlPart",
    #             "role": "dimension",
    #             "type": "TEXT"
    #         },
    #         {
    #             "displayName": "fullPath",
    #             "fullDisplayName": "fullPath",
    #             "isStyled": true,
    #             "name": "fullPath",
    #             "role": "dimension",
    #             "type": "TEXT"
    #         }
    #     ],
    #     "containsLego": false,
    #     "empty": false,
    #     "exportable": true,
    #     "frame": false,
    #     "hasTemplate": false,
    #     "legoProperties": null,
    #     "metaData": {
    #         "filtersAvailable": true,
    #         "orderByAvailable": false,
    #         "pagerAvailable": false,
    #         "searchTextAvailable": false
    #     },
    #     "name": "",
    #     "pager": {
    #         "limit": 20,
    #         "maxPageLimit": 1000,
    #         "offset": 0,
    #         "total": null
    #     },
    #     "rows": [
    #         {
    #             "full_path": "/mnt/static/public/74/reqtxt-2016-09-02_16-48-19-(4501).txt",
    #             "id": "c6509ac7-b410-4f77-8f0b-7c1dfd6a871b",
    #             "url": "http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b"
    #         }
    #     ],
    #     "template": null
    # }


DbQueryService
--------------

Делайте запросы к БД к вашим подключениям

.. code-block:: python

    db_adplatform = META.db("adplatform")
    # Методы query, all, one ОБЯЗАТЕЛЬНО должны возвращать ResultSet (может быть и пустой)
    # Т.е. нельзя делать UPDATE, INSET, DELETE, TRUNCATE, исключение - если в PostgreSQL вы делаете RETURNING

    # Вернет стандартный метовский data_result, где есть rows, columns, meta_data и пр
    data_result = db_adplatform.query("SELECT * FROM users LIMIT 10")

    # Вернет rows из data result
    users = db_adplatform.all("SELECT * FROM users LIMIT 10")

    # Вернет первый элемент из rows или None, если нет первого элемента
    users = db_adplatform.one("SELECT * FROM users WHERE id=4501 LIMIT 1")


    # Метод update используется для запросов, которые НЕ ВОЗВРАЩАЮТ результат в виде ResultSet (в БД)
    db_meta_samples = META.db("meta_samples")
    dr = db_meta_samples.update("""
        UPDATE counters SET inc = inc + 1 WHERE name = :name
    """, {"name": "md_source_update"})
    print(u"dr = %s" % pretty_json(dr))

    dr = db_meta_samples.batch_update("""
        INSERT INTO test_batch_update VALUES (:id, :mytime::timestamp)
        ON CONFLICT(id) DO UPDATE SET mod_time=NOW()
    """, [
        {"id": "py_1", "mytime": "2014-01-01"},
        {"id": "py_2", "mytime": "2014-01-01"},
    ])
    print(u"dr = %s" % pretty_json(dr))