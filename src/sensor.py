from datetime import datetime, date
import numpy as np


class Sensor(object):

    def __init__(
        self,
        visits_per_hour: int = 40,
        perc_break: float = 0.015,
        perc_malfunction: float = 0.035,
    ) -> None:
        """Initialize sensor"""
        self.visits_per_hour = visits_per_hour
        self.perc_break = perc_break
        self.perc_malfunction = perc_malfunction
        self.opening_hour = 8
        self.closing_hour = 19

    def get_number_visitors(self, obs_date: date, obs_hour: int) -> object:
        """Return the number of visitors detected by the sensor
        during the day"""

        # Ensure reproducibility of measurements
        np.random.seed(seed=obs_date.toordinal())

        # The sensor can malfunction sometimes
        failure_number = np.random.random()

        if failure_number < self.perc_break:
            return None

        if failure_number < self.perc_malfunction:
            return 99999999

        # The store is closed on Sunday
        if obs_date.weekday() == 6:
            return 0

        # The store is closed by night
        is_night_hour = (obs_hour < self.opening_hour) or (
            obs_hour >= self.closing_hour
        )
        if is_night_hour:
            return 0

        return self.visits_per_hour


if __name__ == "__main__":
    sensor1 = Sensor(40)
    dt_open = datetime(2025, 1, 24, 12)
    dt_closed = datetime(2025, 1, 24, 1)
    sunday = datetime(2025, 1, 26, 12)

    for item in (dt_open, dt_closed, sunday):
        print(
            f"Datetime : {item}, Date : {item.date()}, Jour : {item.weekday()}, Heure : {item.hour}"
        )
        print(sensor1.get_number_visitors(item.date(), item.hour))
