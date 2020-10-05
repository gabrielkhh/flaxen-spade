from enum import Enum, auto
from os import getenv
from typing import Dict, Tuple

import pendulum
from requests_toolbelt import sessions

from koro.manipulation import first_true
from koro.resolve import Stop, StopFactory


class Seat(Enum):
    AVAILABLE = auto()
    STANDING = auto()
    LIMITED = auto()


class Arrived:
    def __init__(self, payload):
        self.payload = payload

    def get_bus_by_key(self, index: int = 0) -> Dict:
        """
        Access arriving bus data with consecutive keys instead of arbitrary strings.

        :param index: Index of the arriving bus
        :return: Specific bus arrival information
        """
        bus_key_mapping = ["NextBus", "NextBus2", "NextBus3"]
        return self.payload[bus_key_mapping[index]]

    def get_next_bus(self) -> Dict:
        return self.get_bus_by_key(0)

    def get_location(self, index=0) -> Tuple[float, float]:
        target = self.get_bus_by_key(index)

        return float(target["Latitude"]), float(target["Longitude"])

    def get_seating(self, index=0) -> Seat:
        seat_mapping = {
            "SEA": Seat.AVAILABLE,
            "SDA": Seat.STANDING,
            "LSD": Seat.LIMITED,
        }

        return seat_mapping[self.get_bus_by_key(index)["Load"]]

    def is_wheelchair_accessible(self, index=0) -> bool:
        if self.get_bus_by_key(index)["Feature"] == "WAB":
            return True

        return False

    def get_arrival(self, index=0) -> str:
        """
        :param index:
        :return: ISO 8601 format
        """
        return self.get_bus_by_key(index)["EstimatedArrival"]

    def get_friendly_arrival(self, index=0) -> str:
        return pendulum.parse(self.get_arrival(index)).diff_for_humans()

    @property
    def origin(self) -> Stop:
        return StopFactory.load_stop(self.get_next_bus()["OriginCode"])

    @property
    def destination(self) -> Stop:
        return StopFactory.load_stop(self.get_next_bus()["DestinationCode"])

    @property
    def arriving(self) -> str:
        return self.get_arrival()

    @property
    def arriving_at(self) -> str:
        return self.get_friendly_arrival()


class Arrivals:
    def __init__(self, payload):
        self.payload = payload

    @property
    def bus_stop_code(self) -> str:
        return self.payload["BusStopCode"]

    def get_service(self, service_number) -> Arrived:
        """
        :param service_number: Bus service number
        :return: Info about the specific service
        """
        return Arrived(
            first_true(
                self.payload["Services"],
                lambda service: service["ServiceNo"] == service_number,
            )
        )


class Datamall:
    def __init__(self):
        self.http = sessions.BaseUrlSession(getenv("DMALL_URL"))

    def bus_arrivals(self, bus_stop_code: str) -> Arrivals:
        return Arrivals(
            self.http.get("BusArrivalv2", params={"BusStopCode": bus_stop_code}).json()
        )
