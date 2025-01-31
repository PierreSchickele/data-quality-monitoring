import unittest
from datetime import date

from src.sensor import Sensor


class TestSensor(unittest.TestCase):
    def test_weekdays(self):
        for test_day in range(11, 17):
            for test_hour in range(24):
                if 8 <= test_hour <= 18:
                    with self.subTest(i=test_day * 24 + test_hour):
                        visit_sensor = Sensor(0, 40, 0, 0)
                        visit_count = visit_sensor.get_number_visitors(
                            date(2023, 9, test_day), test_hour
                        )
                        self.assertFalse(visit_count == 0)
                else:
                    with self.subTest(i=test_day * 24 + test_hour):
                        visit_sensor = Sensor(0, 40, 0, 0)
                        visit_count = visit_sensor.get_number_visitors(
                            date(2023, 9, test_day), test_hour
                        )
                        self.assertEqual(visit_count, 0)

    def test_sunday_closed(self):
        visit_sensor = Sensor(0, 40, 0, 0)
        visit_count = visit_sensor.get_number_visitors(date(2023, 9, 17), 12)
        self.assertEqual(visit_count, 0)

    def test_with_break(self):
        visit_sensor = Sensor(0, 40, 0, 1)
        visit_count = visit_sensor.get_number_visitors(date(2023, 10, 22), 12)
        self.assertEqual(visit_count, None)

    def test_with_malfunction(self):
        visit_sensor = Sensor(0, 40, 1, 0)
        visit_count = visit_sensor.get_number_visitors(date(2023, 11, 28), 12)
        self.assertEqual(visit_count, 99999999)


if __name__ == "__main__":
    unittest.main()
