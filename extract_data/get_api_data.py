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


def connect_api(store_name: str, queried_date: date, sensor_id: int | None) -> None:
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

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Erreur lors de la requête :", response.status_code)


if __name__ == "__main__":
    date_input = read_date_input()
    store = "Lille"

    if date_input is not None:
        connect_api(store_name=store, queried_date=date_input, sensor_id=None)
