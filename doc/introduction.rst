=====================
Введение
=====================


Install
=======
pip3 install metaappscriptsdk --upgrade --no-cache

Последний резил для Python 2 = 0.1.3
Python 3 начинается с > 0.3.0

Получите файл токен разработчика
Установите developer_settings.json в домашнюю директорию в папку .rwmeta
Например:
 - MacOS: /Users/arturgspb/.rwmeta/developer_settings.json
 - Windows: C:\\Users\\userXXXXXX\\.rwmeta\\developer_settings.json

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
