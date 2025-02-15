from src.store import StoreSensor


def create_app() -> dict:
    """
    Create the available stores in our API
    5 stores, with a different number of sensors,
    a different number of people coming to it,
    as well as different break and malfunction percentages
    (Not realistic, but we keep things simple)
    """

    store_name = ["Lille", "Paris", "Lyon", "Toulouse", "Marseille"]
    store_avg_visit = [3000, 8000, 6000, 2000, 1700]
    perc_malfunction = [0.003, 0.001, 0.008, 0.005, 0.005]
    perc_break = [0.001, 0.0008, 0.005, 0.002, 0]
    number_sensors = [2, 6, 4, 2, 2]

    store_dict = dict()

    for i in range(len(store_name)):
        store_dict[store_name[i]] = StoreSensor(
            store_name[i],
            store_avg_visit[i],
            perc_malfunction[i],
            perc_break[i],
            number_sensors[i],
        )
    return store_dict
