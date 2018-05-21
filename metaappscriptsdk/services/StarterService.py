import json

import collections


class StarterService:
    def __init__(self, app, default_headers):
        """
        Прямые запросы к БД скорее всего уйдут в апи запускатора, так как скорее всего пбудет много БД для тасков запускатора, так как
        Если будет 100500 шард, то врядли все будет в одной БД

        :type app: metaappscriptsdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}
        self.__data_get_cache = {}
        self.__metadb = app.db("meta")
        self.log = app.log

    def update_task_result_data(self, task):
        self.log.info("Сохраняем состояние в БД", {"result_data": task['result_data']})
        self.__metadb.update("""
            UPDATE job.task
            SET result_data=:result_data::jsonb
            WHERE id=:task_id::uuid
            AND service_id=:service_id::job.service_id
        """, {
            "task_id": task.get('taskId'),
            "service_id": task.get('serviceId'),
            "result_data": json.dumps(task['result_data'])
        })

    def await_task(self, task_id, service_id, callback_fn, sleep_sec=15):
        """
        Подождать выполнения задачи запускатора

        :param task_id: ID задачи, за которой нужно следить
        :param service_id: ID сервиса
        :param callback_fn: Функция обратного вызова, в нее будет передаваться task_info
        :param sleep_sec: задержка между проверкой по БД. Не рекомендуется делать меньше 10, так как это может очень сильно ударить по производительности БД
        :return: void
        """
        while True:
            import time
            time.sleep(sleep_sec)
            task_info = self.__metadb.one("""
                SELECT id, service_id, status, result_data 
                FROM job.task
                WHERE id=:task_id::uuid
                AND service_id=:service_id::job.service_id
                LIMIT 1
            """, {
                "task_id": task_id,
                "service_id": service_id,
            })
            self.log.info("Ждем выполнения задачи", {
                "task_info": task_info
            })
            if task_info is None:
                break

            # Уведомляем вызывающего
            callback_fn(task_info)

            if task_info['status'] != 'NEW' and task_info['status'] != 'PROCESSING':
                break
