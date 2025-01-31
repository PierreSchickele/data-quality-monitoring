import sys
from datetime import date

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            year, month, day = [int(v) for v in sys.argv[1].split("-")]
            queried_date = date(year, month, day)
            print(queried_date)
        except ValueError:
            print("Format incorrect. Saisir une date de format : YYYY-MM-DD")
    else:
        print("Indiquer une date en paramètre")
