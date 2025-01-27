from datetime import datetime, date

class Sensor(object):

    def __init__(self):
        self.opening_hour = 8
        self.closing_hour = 19
        self.failure_rate = 0.1
        self.visits_per_hour = 40

    def get_number_visitors(self, obs_date: date, obs_hour: int) -> int:
        # The store is closed on Sunday
        if obs_date.weekday() == 6:
            return 0

        # The store is closed by night
        is_night_hour = ((obs_hour < self.opening_hour)
                        or (obs_hour > self.closing_hour))
        if is_night_hour:
            return 0

        return self.visits_per_hour

if __name__ == "__main__":
    sensor1 = Sensor()
    dt_open = datetime(2025, 1, 24, 12)
    dt_closed = datetime(2025, 1, 24, 1)
    sunday = datetime(2025, 1, 26, 12)

    for item in {dt_open, dt_closed, sunday}:
        print(f"Datetime : {item}, Date : {item.date()}, Jour : {item.weekday()}, Heure : {item.hour}")
        print(sensor1.get_number_visitors(item.date(), item.hour))
