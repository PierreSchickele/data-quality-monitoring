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


def connect_api() -> None:
    url = "https://catfact.ninja/fact"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data["fact"])
    else:
        print("Erreur lors de la requête :", response.status_code)


if __name__ == "__main__":
    connect_api()
