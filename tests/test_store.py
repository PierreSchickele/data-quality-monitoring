import unittest
from datetime import date

from src.store import StoreSensor


class TestStore(unittest.TestCase):
    def test_get_all_traffic(self):
        lille_store = StoreSensor("Lille", 100)
        for test_hour in range(24):
            with self.subTest(i=test_hour):
                if 8 <= test_hour <= 18:
                    visits = lille_store.get_all_traffic(date(2023, 9, 13), test_hour)
                    self.assertEqual(visits, 100)

    def test_get_sensor_traffic(self):
        lille_store = StoreSensor("Lille", 100)
        for test_hour in range(24):
            if 8 <= test_hour <= 18:
                visits = lille_store.get_sensor_traffic(0, date(2023, 9, 13), test_hour)
                self.assertEqual(visits, 81)

    def test_sunday_closed(self):
        lille_store = StoreSensor("Lille", 40)
        for test_hour in range(24):
            if 8 <= test_hour <= 18:
                visits = lille_store.get_sensor_traffic(0, date(2023, 9, 17), test_hour)
                self.assertEqual(visits, 0)


if __name__ == "__main__":
    unittest.main()
