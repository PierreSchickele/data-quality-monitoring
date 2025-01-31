from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.sensor import Sensor
from src import create_app

app = FastAPI()
store_dict = create_app()


@app.get("/")
def visit(
    store_name: str,
    year: int,
    month: int,
    day: int,
    sensor_id: int | None = None,
) -> JSONResponse:
    # If the store is not in the dictionary
    if not (store_name in store_dict.keys()):
        return JSONResponse(status_code=404, content="Store Not found")

    # Check the value of sensor_id
    nb_sensors = store_dict[store_name].number_sensors
    if sensor_id and (sensor_id >= nb_sensors or sensor_id < 0):
        return JSONResponse(
            status_code=404, content=f"Sensor_id should be between 0 and {nb_sensors-1}"
        )

    # Check the year
    if year < 2019:
        return JSONResponse(status_code=404, content="No data before 2019")

    # Check the date
    try:
        obs_date = date(year, month, day)
    except TypeError:
        return JSONResponse(status_code=404, content="Enter a valid date")

    # Check the date is in the past
    if date.today() < obs_date:
        return JSONResponse(status_code=404, content="Choose a date in the past")

    # If no sensor choose return the visit for the whole store
    if sensor_id is None:
        visit_counts = {
            hour: store_dict[store_name].get_all_traffic(date(year, month, day), hour)
            for hour in range(24)
        }
    else:
        visit_counts = {
            hour: store_dict[store_name].get_sensor_traffic(
                sensor_id, date(year, month, day), hour
            )
            for hour in range(24)
        }

    try:
        max_visit_counts = max(
            visit_counts[k] for k in visit_counts if type(visit_counts[k]) == int
        )
    except TypeError:
        return JSONResponse(status_code=404, content="Output is not a number")

    if max_visit_counts <= 0:
        return JSONResponse(
            status_code=404, content="The store was closed try another date"
        )

    return JSONResponse(status_code=200, content=visit_counts)
