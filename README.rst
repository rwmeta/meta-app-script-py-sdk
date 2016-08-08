=========================
Meta App Script SDK
=========================


Install
=======
pip install metaappscriptsdk


Usage
=====
.. code-block:: python

    # coding=utf-8
    import logging
    import starter_api
    from metaappscriptsdk import MetaApp

    # Инициализация приложения
    # конфигурирует логгер и пр.
    META = MetaApp(service_id='MyService', debug=True)  # debug для того, чтобы не писать логи в службу логирования

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