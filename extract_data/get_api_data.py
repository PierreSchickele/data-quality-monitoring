import csv
import os
import sys
from datetime import date
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
    url = endpoint + f"?store_name={store_name}&year={year}&month={month}&day={day}"

    if sensor_id is not None:
        url += f"&sensor_id={sensor_id}"

    response = requests.get(url)

    if response.status_code != 200:
        print("Code of the API request:", response.status_code)
        return response.json()

    data = response.json()
    data["date"] = queried_date.strftime("%Y-%m-%d")
    data["store_name"] = store_name
    if sensor_id is not None:
        data["sensor_id"] = sensor_id

    return data


def get_data() -> str:
    """
    Print the API response into a string.
    :return: a string which contains API response (JSON type or error)
    """
    user_input = sys.argv

    # Check if there is enough parameters
    if len(user_input) <= 2:
        raise Exception("Error: not enough parameters")

    # Check if the first parameter is a date
    date_input = read_date_input(user_input[1])
    if date_input is None:
        raise TypeError("Error: wrong type of date")

    # Second parameter should be a store
    store_name_input = user_input[2]

    # If more parameters, check if it is an integer
    if len(user_input) > 3:
        try:
            sensor_id_input = int(user_input[3])
            return connect_api(store_name_input, date_input, sensor_id_input)
        except ValueError:
            raise TypeError("Error: wrong type of sensor id")
    else:
        return connect_api(store_name_input, date_input)


def write_csv():
    # Write the output of get_data
    output = get_data()

    # Check type of json data
    if isinstance(output, str) and output.__contains__("closed"):
        print(output)
        return 1

    if not isinstance(output, dict):
        print(output)
        raise Exception("Error: Unexpected JSON format")

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

    print(f"Données enregistrées dans {filename}")
    return 0


if __name__ == "__main__":
    write_csv()
