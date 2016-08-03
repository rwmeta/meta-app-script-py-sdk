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
    META = MetaApp(debug=True)  # debug для того, чтобы не писать логи в службу логирования

    # работает стандартный логгер
    logging.info('Hello, from Meta App Script!')

    # Поставновка задач в Запускатор
    starter_api.build_submit('YOUR_SERVICE')
    # или
    META.starter.build_submit('YOUR_SERVICE')

