# coding=utf-8
import time


class BulkLogger:
    def __init__(self, log, log_message, total, part_log_time_minutes):
        self.__log = log
        self.__begin_time = time.time()

        self.__log_message = log_message
        self.__part_log_time_seconds = part_log_time_minutes * 60
        self.__counter = 0

        if total <= 0:
            self.__log.info('Нет элементов для логирования. Вероятно список массив пустой')
            total = None

        self.__total = total

    def try_log_part(self, context=None, with_start_message=True):
        """
        Залогировать, если пришло время из part_log_time_minutes
        :return: boolean Возвращает True если лог был записан
        """
        if context is None:
            context = {}
        self.__counter += 1
        if time.time() - self.__begin_time > self.__part_log_time_seconds:
            self.__begin_time = time.time()
            context['count'] = self.__counter
            if self.__total:
                context['percentDone'] = int(self.__counter * 100 / self.__total)
                context['total'] = self.__total
            self.__log.info(msg=self.__log_message, context=context)
            return True
        elif self.__counter == 1:
            if with_start_message:
                self.__log.info(u"Начали цикл: " + self.__log_message)
            return True
        return False

    def finish(self):
        self.__log.info(u"Закончили цикл: " + self.__log_message)
