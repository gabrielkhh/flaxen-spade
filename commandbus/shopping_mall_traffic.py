from koro.dataset import CsvLoader, JsonLoader
from koro.manipulation import dataset_path
import json

stations_dict = {}


def stations_init(stations_info):
    # Create a dictionary tying the stations code to their names.
    # print(stations_info)
    for station in stations_info:
        code = f"{station['stn_code']}"
        stations_dict[code] = f"{station['mrt_station_english']}"


def mall_traffic():
    temp_month = 8
    temp_month_name = "August"

    reader = CsvLoader()
    entries = reader.load_file("od/mangled/BY_TAPOUT_transport_node_train_202008.csv")
    stations_info = CsvLoader(delimiter="\t").load_file("raw_other/train-station.csv")

    stations_init(stations_info)

    # locations_dict = {"Serangoon": "Nex", "Bishan": "Junction 8", "Ang Mo Kio": "AMK Hub", "Yishun": "Northpoint"}

    print(stations_dict)

    count = 1

    for entry in entries:
        station_code = f"{entry['PT_CODE']}"
        station_name = stations_dict[station_code.split('/')[0]]
        print("%s and %d" % (station_name, count))
        count += 1

    # print("")

