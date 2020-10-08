from os import path

import regex
from flask import current_app

from koro.dataset import CsvLoader, JsonLoader
from koro.manipulation import dataset_path


def is_matched(match, to_match) -> bool:
    return to_match == match[1] or to_match == match[2] or to_match == match[3]


def run():
    headers = "station_code,mrt_station,mrt_line,lat,long\n"
    path_to_merged = dataset_path("merged/train-data.csv")

    coordinates = JsonLoader().load_file("raw_other/rails.geojson")
    stations = CsvLoader(delimiter="\t").load_file("raw_other/train-station.csv")

    with open(path_to_merged, "w") as file:
        file.write(headers)
        for station in stations:

            found_coordinate = None
            for coordinate in coordinates["features"]:
                if coordinate["properties"]["stop_type"] != "station":
                    break

                match = regex.match(
                    r"(\w+)(?:-(\w+))?(?:-(\w+))?",
                    coordinate["properties"]["station_codes"],
                )
                if is_matched(match, station["stn_code"]):
                    found_coordinate = coordinate
                    break

            if found_coordinate is None:
                print(f"Not found: {station['stn_code']}. Skipping")
                continue

            long, lat = found_coordinate["geometry"]["coordinates"]

            file.write(
                "{},{},{},{},{}\n".format(
                    station["stn_code"],
                    station["mrt_station_english"],
                    station["mrt_line_english"].rstrip(),
                    lat,
                    long,
                )
            )
