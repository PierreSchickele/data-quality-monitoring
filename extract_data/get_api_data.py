import csv
import os
from datetime import date, timedelta
import requests
import argparse


def connect_api(store_name: str, queried_date: date, sensor_id: int | None = None):
    """
    Connect to the API, and print the JSON output
    :param store_name: name of the store
    :param queried_date: date of the observation
    :param sensor_id: id of the sensor (optional)
    :return: The result of the request in dict format
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


def write_csv(output, exec_hour):
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

    # Ensure the directory "data/raw" exists
    os.makedirs("data/raw", exist_ok=True)

    # Name the CSV file
    filename = f"data/raw/store_visits_{year}-{month}.csv"

    # Check if the file already exists
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    # Open the file in "append" mode (a)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the CSV header only if the file is empty
        if not file_exists:
            writer.writerow(
                ["date", "hour", "store_name", "sensor_id", "visits_count", "unit"]
            )

        unit = "visitors"
        visits_count = output.get(str(exec_hour), "")
        writer.writerow(
            [
                date_str,
                exec_hour,
                store_name,
                sensor_id if sensor_id is not None else "ALL",
                "" if date_str == "2024-01-02" else visits_count,
                "objects" if date_str == "2024-01-01" else unit,
            ]
        )

    return 0


def parse_execution_datetime() -> tuple[date, int]:
    """Parse execution date and hour."""
    parser = argparse.ArgumentParser(description="Extract store visit data.")
    parser.add_argument(
        "--execution_date",
        type=str,
        default=date.today().strftime("%Y-%m-%d"),
        help="Execution date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--execution_hour",
        type=int,
        help="Execution hour (0-23).",
        required=True,
    )
    args = parser.parse_args()
    return date.fromisoformat(args.execution_date), args.execution_hour


def main():
    stores = ["Lille", "Marseille", "Toulouse"]
    sensors = [None, 0, 1]

    exec_date, exec_hour = parse_execution_datetime()

    for store in stores:
        for sensor in sensors:
            output = connect_api(store, exec_date, sensor)
            write_csv(output, exec_hour)


if __name__ == "__main__":
    main()
