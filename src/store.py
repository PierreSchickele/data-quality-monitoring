from datetime import date
import numpy as np
from src.sensor import Sensor


class StoreSensor:

    def __init__(
        self,
        name: str,
        avg_visit: int,
        perc_malfunction: float = 0,
        perc_break: float = 0,
        number_sensors: int = 2,
    ) -> None:
        """Initialize a store"""
        self.name = name
        self.number_sensors = number_sensors
        self.sensors = list()

        # To always get the same result when asking for the same store
        seed = np.sum(list(self.name.encode("ascii")))
        np.random.seed(seed=seed)

        # Pareto's law
        shape, size, lower = 0.1, number_sensors, 1
        weights = np.random.pareto(shape, size) + lower
        traffic_percentage = (weights / sum(weights)).tolist()
        np.random.shuffle(traffic_percentage)

        # Initialisation of the store's sensors
        for i in range(number_sensors):
            sensor = Sensor(
                i,
                round(traffic_percentage[i] * avg_visit),
                perc_malfunction,
                perc_break,
            )
            self.sensors.append(sensor)

    def get_sensor_traffic(self, sensor_id: int, obs_date: date, obs_hour: int) -> int:
        """Return the traffic for one sensor at a date"""
        return self.sensors[sensor_id].get_number_visitors(obs_date, obs_hour)

    def get_all_traffic(self, obs_date: date, obs_hour: int) -> int | None:
        """Return the traffic for all sensors of the store at a date"""
        visits = [
            self.sensors[i].get_number_visitors(obs_date, obs_hour)
            for i in range(self.number_sensors)
        ]
        return (
            None
            if all(v is None for v in visits)
            else sum(v for v in visits if v is not None)
        )
