import operator
from math import asin, cos, radians, sin, sqrt
from typing import Dict, List, Tuple, Union

import requests as http

from cache import cache
from koro.dataset import CsvLoader, JsonLoader
from koro.resolve import Stop, TrainStation

Coordinate = Tuple[float, float]


def haversine(first: Coordinate, second: Coordinate) -> float:
    """
    Calculate the great circle distance between two points on the earth.

    :param first: First point as a tuple of (lat, long)
    :param second: Second point as a tuple of (lat, long)
    :return:
    """

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [*first, *second])

    longitude_difference = lon2 - lon1
    latitude_difference = lat2 - lat1
    chord_length = (
        sin(latitude_difference / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(longitude_difference / 2) ** 2
    )
    angular_distance_in_radians = 2 * asin(sqrt(chord_length))
    radius_of_earth = 6371

    return round(angular_distance_in_radians * radius_of_earth, 2)


def resolve_coordinates(location_name: str) -> Dict[str, float]:
    response = http.post(
        "https://places-dsn.algolia.net/1/places/query",
        json={"query": location_name, "language": "en", "countries": "sg"},
    ).json()

    # Number of results
    if response["nbHits"] <= 0:
        raise ValueError("No results!")

    return response["hits"][0]["_geoloc"]


class Nearest:
    def __init__(self):
        self.latitude = None
        self.longitude = None

    def location(self, place) -> "Nearest":
        coordinate = resolve_coordinates(place)
        self.latitude = coordinate["lat"]
        self.longitude = coordinate["lng"]

        return self

    def raw_location(self, latitude, longitude) -> "Nearest":
        self.latitude = latitude
        self.longitude = longitude

        return self

    def raise_if_empty(self):
        if self.latitude is None and self.longitude is None:
            raise ValueError(f"Empty coordinates!")

    def get_location(self) -> Tuple[float, float]:
        if self.latitude is None and self.longitude is None:
            raise ValueError(f"Empty coordinates!")

        return self.latitude, self.longitude

    def is_within_limit(self, latitude, longitude, limit) -> Union[bool, float]:
        distance = haversine(self.get_location(), (latitude, longitude))
        if distance < limit:
            return distance

        return False

    def bus_stop(self, limit: float) -> List[Tuple[float, Stop]]:
        stops = JsonLoader().load_file("static/stops.json")

        matched_stops = [
            (distance, Stop(code, stop))
            for code, stop in stops.items()
            if (distance := self.is_within_limit(stop["lat"], stop["lng"], limit))
        ]

        return sorted(matched_stops, key=operator.itemgetter(0))

    def train_station(self, limit: float) -> List[Tuple[float, TrainStation]]:
        stations = CsvLoader().load_file("merged/train-data.csv")

        matched_stations = [
            (distance, TrainStation(station))
            for station in stations
            if (
                distance := self.is_within_limit(
                    float(station["lat"]), float(station["long"]), limit
                )
            )
        ]

        return sorted(matched_stations, key=operator.itemgetter(0))
