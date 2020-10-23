import json

from tabulate import tabulate

from koro.dataset import CsvLoader, JsonLoader
from koro.geo import Nearest
from koro.manipulation import dataset_path
from koro.resolve import TrainStationFactory

malls_dict = {}
results_dict = {}
tap_out_dict = {}
hours_tuple = 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
volume_list_weekday = []
volume_list_weekends = []
table_headers = [
    "Shopping Mall Name",
    "Nearest MRT Station",
    "Type of Day",
    "Hour of Day",
    "Volume of People",
]
table_list_weekday = []
table_list_weekends = []


def compute_volume(mall_name, station_name):
    constant_id_weekday = "WEEKDAY" + station_name
    constant_id_weekends = "WEEKENDS/HOLIDAY" + station_name
    volume_list_weekday.clear()
    volume_list_weekends.clear()

    for hour in hours_tuple:
        id_weekday = constant_id_weekday + str(hour)
        id_weekends = constant_id_weekends + str(hour)
        volume_list_weekday.append({"hour": hour, "volume": tap_out_dict[id_weekday]})
        volume_list_weekends.append({"hour": hour, "volume": tap_out_dict[id_weekends]})
        # volume_list_weekday.append(tap_out_dict[id_weekday])
        # volume_list_weekends.append(tap_out_dict[id_weekends])
        table_list_weekday.append(
            [mall_name, station_name, "Weekday", hour, tap_out_dict[id_weekday]]
        )
        table_list_weekends.append(
            [
                mall_name,
                station_name,
                "Weekends/Holiday",
                hour,
                tap_out_dict[id_weekends],
            ]
        )


def mall_traffic():
    temp_month_name = "June"

    reader = CsvLoader()
    json_reader = JsonLoader()
    malls_coordinates = json_reader.load_file("static/mallCoordinates.json")
    entries = reader.load_file("od/mangled/BY_TAPOUT_transport_node_train_202006.csv")

    # Looping our LTA data object from the csv file and store the values we want (Tap out vol) in a dictionary
    for entry in entries:
        try:
            station = TrainStationFactory.load_station(
                entry["PT_CODE"].split("/")[0]
            )  # an instance of TrainStation
            custom_key = entry["DAY_TYPE"] + station.name + entry["TIME_PER_HOUR"]
            tap_out_dict[custom_key] = int(entry["TOTAL_TAP_OUT_VOLUME"])
        except ValueError:
            continue

    # Looping through the mallCoordinates json object and tying the volume based on nearest MRT to the mall via long & lat data.
    for mall_name, coordinates in malls_coordinates.items():
        train = Nearest()
        # Get the closest train stations within 3km of this location
        list_of_stations = train.raw_location(
            coordinates["latitude"], coordinates["longitude"]
        ).train_station(limit=3)
        distance, closest_train = list_of_stations[
            0
        ]  # Tuple of (distance_in_km, Instance of TrainStation)

        # Get the volume of people
        compute_volume(mall_name, closest_train.name)

        mall_data = {
            "stationName": closest_train.name,
            "weekday": volume_list_weekday,
            "weekends": volume_list_weekends,
        }
        malls_dict[mall_name] = mall_data

    results_dict[temp_month_name] = malls_dict

    # Table will be presented in weekday data first followed by weekends/holiday data
    table_list = table_list_weekday + table_list_weekends
    table_list.insert(0, table_headers)

    print(tabulate(table_list, headers="firstrow", tablefmt="psql"))

    with open(
        dataset_path("results/shopping-mall-passenger-volume.json"), "w+"
    ) as file:
        json.dump(results_dict, file)
