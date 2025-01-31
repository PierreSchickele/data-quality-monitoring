import sys
from datetime import datetime, date
import numpy as np


class Sensor(object):

    def __init__(
        self,
        sensor_id: int,
        visits_per_hour: int = 100,
        perc_malfunction: float = 0,
        perc_break: float = 0,
    ) -> None:
        """Initialize sensor"""
        self.sensor_id = sensor_id
        self.visits_per_hour = visits_per_hour
        self.perc_malfunction = perc_malfunction
        self.perc_break = perc_break
        self.opening_hour = 8
        self.closing_hour = 19

    def get_number_visitors(self, obs_date: date, obs_hour: int) -> int | None:
        """Return the number of visitors detected by the sensor
        during the day"""

        # Ensure reproducibility of measurements
        seed_number = (obs_date.toordinal() - 1) * 240 + obs_hour * 10 + self.sensor_id
        np.random.seed(seed=seed_number)

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
    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
    else:
        year, month, day = 2023, 10, 25
    queried_date = date(year, month, day)

    capteur = Sensor(40)

    output_dict = {
        hour: capteur.get_number_visitors(queried_date, hour) for hour in range(24)
    }

    print(output_dict)
