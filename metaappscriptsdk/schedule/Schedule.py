# coding=utf-8

import datetime

import croniter as croniter


class Schedule:
    def get_next_time(self, expr_list, as_string=False, now=None):
        """
        Расчитываем время следуещего запуска
        """
        if now is None:
            now = datetime.datetime.now()

        min_date = None
        for expr in expr_list:
            cron = croniter.croniter(expr.get('value'), now)
            val_ = cron.get_next(datetime.datetime)
            if min_date is None or val_ < min_date:
                min_date = val_
        if as_string and min_date:
            return min_date.strftime("%Y-%m-%d %H:%M:%S")
        return min_date
