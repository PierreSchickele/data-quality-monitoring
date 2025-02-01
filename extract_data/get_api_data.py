import sys
from datetime import date
import requests


def read_date_input() -> date | None:
    """
    Verify that the parameter given by the user is a date in YYYY-MM-DD format,
    then return the date.
    :return: The date in YYYY-MM-DD format
    """
    if len(sys.argv) > 1:
        try:
            year, month, day = [int(v) for v in sys.argv[1].split("-")]
            queried_date = date(year, month, day)
            print(queried_date)
            return queried_date
        except ValueError:
            print("Format incorrect. Saisir une date de format : YYYY-MM-DD")
    else:
        print("Indiquer une date en paramètre")


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
