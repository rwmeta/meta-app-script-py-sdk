=====================
RPC Meta Services
=====================

Это API внутренних функций Меты, все эти функции доступны вам через редактор в Web-интерфейсе

SettingsService
---------------

Рассчитан на чтение параметров из мета конфигурации
Это удобно когда вы хотите хранить ссылки/токены для вшешних api, какие-то глобальные или частные настройки.
При этом вы хотите дать некоторым пользователям вохможность это редактировать через интерфейс

Примеры
-------

`Список примеров
<https://github.com/rw-meta/meta-app-script-py-sdk/tree/master/metaappscriptsdk/examples/settings_api>`_


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


Отдельно стоит упомянуть про LoadData Api
Этот API позваоляет как в BigQuery создавать таблицу у казанной БД и потоково загружать в нее данные из файла формата TSV
Это позволяет ускорять вставку данных в таблицу от 2 до 4-5 раз.

ВАЖНО! Данные всегда добавляются в указанную таблицу и никакой очистки старых данных нет - вы должны почистить таблицу сами, если вам это нужно

.. code-block:: python

    import os
    from metaappscriptsdk import MetaApp

    META = MetaApp()

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
    db.upload_data(upload_file, configuration)


SettingsService
---------------

Получайте настройки из стандартного источника настроек

.. code-block:: python

    settings = META.SettingsService

    # Вернуть только данные
    rwapp_conf = settings.data_get("rwapp")

    # Полная информация о данных + данные
    full_rwapp_conf = settings.data_get("rwapp", data_only=False)

    onec_url = settings.config_param("rwapp", "app.onec.url")
