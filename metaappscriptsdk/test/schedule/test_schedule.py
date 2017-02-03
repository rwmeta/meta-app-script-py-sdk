import datetime
from unittest import TestCase

from metaappscriptsdk.schedule.Schedule import Schedule


class TestSchedule(TestCase):
    def test_get_next_time(self):
        now = datetime.datetime(2005, 1, 1, 0, 0)
        schedule = Schedule()
        exprs = [
            {
                "value": "0 0 * * *"
            },
        ]
        actual = schedule.get_next_time(exprs, True, now)
        self.assertEqual('2005-01-02 00:00:00', actual)

    def test_get_next_time_min_date(self):
        now = datetime.datetime(2005, 1, 1, 0, 0)
        schedule = Schedule()
        exprs = [
            {
                "value": "0 0 * * *"
            },
            {
                "value": "10 4 3 * *"
            }
        ]
        actual = schedule.get_next_time(exprs, False, now)
        self.assertEqual(datetime.datetime(2005, 1, 3, 4, 10), actual)
