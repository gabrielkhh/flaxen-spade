from math import asin, cos, radians, sin, sqrt
from typing import Dict, Tuple

import requests as http

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
    )

    return response.json()["hits"][0]["_geoloc"]
