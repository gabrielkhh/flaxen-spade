from koro.dataset import CsvLoader
from koro.resolve import TrainStationFactory
from koro.manipulation import dataset_path
import json
from tabulate import tabulate


results = {}
six_list = []
seven_list = []
eight_list = []

def run():
    reader = CsvLoader()

    entries = reader.load_file("od/mangled/BY_TAPIN_transport_node_train_202008.csv")

    for entry in entries:
        pt_code = entry["PT_CODE"]
        hour = entry["TIME_PER_HOUR"]
        tap_in = entry["TOTAL_TAP_IN_VOLUME"]


        # AM peak --> 6am - 9am
        if entry["DAY_TYPE"] == "WEEKDAY":
            if hour in ['6', '7', '8']:

                station_obj = TrainStationFactory.load_station(pt_code)
                station_name = station_obj.name
                if hour == '6':
                    six_list.append({"hour": hour, "pt_code": pt_code, "station_name": station_name, "tap_in": tap_in})
                elif hour == '7':
                    seven_list.append({"hour": hour, "pt_code": pt_code, "station_name": station_name, "tap_in": tap_in})
                elif hour == '8':
                    eight_list.append({"hour": hour, "pt_code": pt_code, "station_name": station_name, "tap_in": tap_in})

    results["6"] = six_list[:5]
    results["7"] = seven_list[:5]
    results["8"] = eight_list[:5]
    outer_list = []


    for index in range(6,9):
        result_list = []
        for data in results[str(index)]:
            result_dict = {"pt_code": data["pt_code"], "tap_in": data["tap_in"], "name": data["station_name"]}
            result_list.append(result_dict)

        outer_list.append({"hour": index, "stations": result_list})

    print(outer_list)
    # print(tabulate([["hour", "pt_code", "station_name", "tap_in", "tap_out"], [hour, pt_code, station_name, tap_in]],headers="firstrow"))

    with open(dataset_path("results/popular_stations.json"), "w+") as file:
        json.dump(outer_list, file)

