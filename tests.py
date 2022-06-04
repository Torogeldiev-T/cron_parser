import unittest
from cron_parser import Cron


class ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.argument = "1-4,5 0 1,15 */5,9 1-5 /usr/bin/find"
        self.cron = Cron(self.argument)
        self.cron.parse()

    def test_minute_range(self):
        self.assertCountEqual(self.cron.minutes, [1, 2, 3, 4, 5])

    def test_hour_single(self):
        self.assertCountEqual(self.cron.hours, [0])

    def test_months_slash_and_comma(self):
        self.assertCountEqual(self.cron.months, [5, 10, 9])


class ParseMinuteTestCase(unittest.TestCase):
    def setUp(self):
        self.argument = "0,1,2,3,4,5,50-59/2 20/2 1,15 1,5-10/2 */1 /usr/bin/find"
        self.cron = Cron(self.argument)
        self.cron.parse()

    def test_minute_comma_slash_hyphen(self):
        self.assertCountEqual(self.cron.minutes, [0, 1, 2, 3, 4, 5, 50, 52, 54, 56, 58])

    def test_hour_slash(self):
        self.assertCountEqual(self.cron.hours, [20, 22, 24])

    def test_days_of_week_months(self):
        self.assertCountEqual(self.cron.days_week, [1, 2, 3, 4, 5, 6, 7])
        self.assertCountEqual(self.cron.months, [1, 6, 8, 10])


class ValidateTestCase(unittest.TestCase):
    def setUp(self):
        self.argument_1 = "1,2,3,4,5,63 20/2 1,15 1,5-10/2 */1 /usr/bin/find"
        self.cron_1 = Cron(self.argument_1)

        self.argument_2 = "1,2,3,4,5 20/2,+ 1,15 1,5-10/2 */1 /usr/bin/find"
        self.cron_2 = Cron(self.argument_2)

    def test_runtime_error_minute(self):
        self.assertRaises(RuntimeError, self.cron_1.parse)

    def test_runtime_hour_plus_char(self):
        self.assertRaises(RuntimeError, self.cron_2.parse)
