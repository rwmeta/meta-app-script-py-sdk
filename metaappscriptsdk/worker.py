# coding=utf-8
import json
import os

import time


class Worker:
    def __init__(self, app, stdin):
        """
        :type app: metaappscriptsdk.MetaApp
        :type stdin: basestring
        """
        self.__app = app
        self.__raw_tasks = json.loads(stdin)
        self.debug_tasks = None
        self.__current_task = None

    def single_task(self, main_fn=None):
        self.__run(main_fn, 'single')

    def multiple_task(self, main_fn=None):
        self.__run(main_fn, 'multiple')

    def ignore_task(self, main_fn=None):
        self.__run(main_fn, 'ignore')

    def __run(self, main_fn, resolver_type):
        tasks = self.__get_tasks()
        if not tasks:
            return

        log = self.__app.log
        log.info(u'Старт')
        begin_time = time.time()
        try:
            log.set_entity("session_id", tasks[0].get("sessionId"))
            if resolver_type == 'multiple':
                main_fn(tasks)
            elif resolver_type == 'single':
                for task in tasks:
                    self.__current_task = task
                    log.set_entity("task_id", task.get("id"))
                    main_fn(task)
            elif resolver_type == 'ignore':
                for ignore_ in tasks:
                    log.set_entity("task_id", ignore_.get("id"))
                    main_fn()
        except Exception as e:
            log.critical(u'Воркер упал из-за неожиданного исключения', {"e": e})
            os._exit(1)
        finally:
            log.info(u'Стоп', {"seconds": int(time.time() - begin_time)})

    def __get_tasks(self):
        tasks = []
        if self.__app.debug:
            tasks = self.debug_tasks

        if not tasks:
            tasks = self.__raw_tasks
        return tasks

    prop = property()

    @prop.getter
    def current_task(self):
        return self.__current_task