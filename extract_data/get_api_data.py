import csv
import os
from datetime import date, timedelta
import requests


def read_date_input(input_date: str) -> date | None:
    """
    Verify that the parameter given by the user is a date in YYYY-MM-DD format,
    then return the date.
    :param input_date: parameter entered by the user
    :return: The date in YYYY-MM-DD format
    """
    try:
        year, month, day = [int(v) for v in input_date.split("-")]
        queried_date = date(year, month, day)
        return queried_date
    except ValueError:
        print("Incorrect value. The date format should be: YYYY-MM-DD")


def connect_api(store_name: str, queried_date: date, sensor_id: int = None):
    """
    Connect to the API, and print the JSON output
    :param store_name: name of the store
    :param queried_date: date of the observation
    :param sensor_id: id of the sensor (optional)
    :return: no output
    """
    year, month, day = queried_date.year, queried_date.month, queried_date.day

    endpoint = "http://127.0.0.1:8000"
    url = f"{endpoint}?store_name={store_name}&year={year}&month={month}&day={day}"
    if sensor_id is not None:
        url += f"&sensor_id={sensor_id}"

    response = requests.get(url)

    if response.status_code != 200:
        print("API request failed with status code:", response.status_code)
        return response.json()

    data = response.json()
    data["date"] = queried_date.strftime("%Y-%m-%d")
    data["store_name"] = store_name
    if sensor_id is not None:
        data["sensor_id"] = sensor_id

    return data


def write_csv(output):
    # Check type of json data
    if isinstance(output, str) and output.__contains__("closed"):
        print(output)
        return 1

    if not isinstance(output, dict):
        print("Error: Unexpected JSON format")
        return 1

    # Extract date, store_name and sensor_id
    date_str = output.pop("date")
    store_name = output.pop("store_name")
    sensor_id = output.pop("sensor_id", None)

    # Extract the year and the month from the "date" field
    year, month = date_str.split("-")[:2]

    # Name the CSV file
    filename = f"data/raw/store_visits_{year}-{month}.csv"

    # Check if the file already exists
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    # Open the file in "append" mode (a)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the CSV header only if the file is empty
        if not file_exists:
            writer.writerow(["date", "hour", "store_name", "sensor_id", "visits_count"])

        for hour, visits_count in output.items():
            writer.writerow(
                [
                    date_str,
                    int(hour),
                    store_name,
                    sensor_id if sensor_id is not None else "ALL",
                    visits_count,
                ]
            )

    print(
        f"Day: {date_str}, "
        f"store: {store_name}, "
        f"sensor: {sensor_id if sensor_id is not None else 'ALL'}"
    )
    print(f"Data saved to {filename}")
    return 0


def main():
    stores = ["Lille", "Marseille", "Toulouse"]
    years = ["2024"]
    months = [f"{i:02}" for i in range(1, 13)]
    sensors = []

    for year in years:
        for month in months:
            first_day = date(int(year), int(month), 1)
            last_day = (first_day.replace(day=28) + timedelta(days=4)).replace(
                day=1
            ) - timedelta(days=1)

            for day in range(1, last_day.day + 1):
                date_str = f"{year}-{month}-{day:02}"
                queried_date = read_date_input(date_str)

                for store in stores:
                    if sensors:
                        for sensor in sensors:
                            output = connect_api(store, queried_date, sensor)
                            write_csv(output)
                    else:
                        output = connect_api(store, queried_date)
                        write_csv(output)


if __name__ == "__main__":
    main()
