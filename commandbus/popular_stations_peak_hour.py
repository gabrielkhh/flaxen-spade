import json
from koro.dataset import CsvLoader
from koro.manipulation import dataset_path
from koro.resolve import TrainStationFactory
from tabulate import tabulate

results = {}
six_list = []
seven_list = []
eight_list = []


def run(count):
    reader = CsvLoader()
    entries = reader.load_file("od/mangled/BY_TAPIN_transport_node_train_202008.csv")
    count = int(count)  # to sort by value input by user

    for entry in entries:
        pt_code = entry["PT_CODE"]
        hour = entry["TIME_PER_HOUR"]
        tap_in = entry["TOTAL_TAP_IN_VOLUME"]

        # Weekday AM peak --> 6am - 9am
        if entry["DAY_TYPE"] == "WEEKDAY":
            if hour in ["6", "7", "8"]:
                station_obj = TrainStationFactory.load_station(pt_code)
                station_name = station_obj.name
                if hour == "6":
                    six_list.append(
                        {
                            "hour": hour,
                            "pt_code": pt_code,
                            "station_name": station_name,
                            "tap_in": tap_in,
                        }
                    )
                elif hour == "7":
                    seven_list.append(
                        {
                            "hour": hour,
                            "pt_code": pt_code,
                            "station_name": station_name,
                            "tap_in": tap_in,
                        }
                    )
                elif hour == "8":
                    eight_list.append(
                        {
                            "hour": hour,
                            "pt_code": pt_code,
                            "station_name": station_name,
                            "tap_in": tap_in,
                        }
                    )

    results["6"] = six_list[:count]
    results["7"] = seven_list[:count]
    results["8"] = eight_list[:count]
    outer_list = []

    for hour in range(6, 9):
        result_list = []
        for data in results[str(hour)]:
            result_dict = {"pt_code": data["pt_code"], "station_name": data["station_name"], "tap_in": data["tap_in"]}
            result_list.append(result_dict)

            # print in tabulate format
            """print(
                tabulate([["hour", "pt_code", "station_name", "tap_in"],[index, data["pt_code"], data["station_name"],
                                                                         data["tap_in"]],],headers="firstrow",)+"\n")"""

        outer_list.append({"hour": hour, "stations": result_list})

    print("Top %d  MRT Station(s) during Weekday Peak Hours" % count)
    print(outer_list) # print in JSON format
    with open(dataset_path("results/popular_stations.json"), "w+") as file:
        json.dump(outer_list, file)
