import json

from tabulate import tabulate

from koro.dataset import CsvLoader
from koro.manipulation import dataset_path
from koro.resolve import TrainStationFactory

results = {}
hours = [6, 7, 8, 9, 12, 18, 19, 20]


def run(count):
    reader = CsvLoader()
    entries = reader.load_file("od/mangled/BY_TAPIN_transport_node_train_202008.csv")
    count = int(count)  # to sort by value input by user

    for entry in entries:
        pt_code = entry["PT_CODE"]
        hour = entry["TIME_PER_HOUR"]
        tap_in = entry["TOTAL_TAP_IN_VOLUME"]

        # Weekday AM peak --> 6am - 9am
        if entry["DAY_TYPE"] == "WEEKDAY" and int(hour) in hours:
            station_obj = TrainStationFactory.load_station(pt_code)
            station_name = station_obj.name
            if hour not in results:
                results[hour] = []

            if len(results[hour]) < count:
                results[hour].append(
                    {
                        "pt_code": pt_code,
                        "station_name": station_name,
                        "tap_in": tap_in,
                    }
                )

            # print in tabulate format
            """print(
                tabulate([["hour", "pt_code", "station_name", "tap_in"],[index, data["pt_code"], data["station_name"],
                                                                         data["tap_in"]],],headers="firstrow",)+"\n")"""

    # print("Top %d  MRT Station(s) during Weekday Peak Hours" % count)
    # print(outer_list)  # print in JSON format
    with open(dataset_path("results/popular_stations.json"), "w+") as file:
        json.dump({int(x): results[x] for x in results.keys()}, file, sort_keys=True, indent=4)
