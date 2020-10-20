from enum import Enum, auto
from os import getenv
from typing import Dict, List, Tuple

import pendulum
from requests_toolbelt import sessions

from koro.manipulation import first_true
from koro.resolve import BusService, BusServiceFactory, Stop, StopFactory


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

    def has_already_left(self, index=0) -> bool:
        return self.get_arrival(index).is_past()

    def is_wheelchair_accessible(self, index=0) -> bool:
        if self.get_bus_by_key(index)["Feature"] == "WAB":
            return True

        return False

    def get_arrival(self, index=0) -> pendulum.DateTime:
        """
        :param index:
        :return: Instance of pendulum
        """
        if (arriving := self.get_bus_by_key(index)["EstimatedArrival"]) is None:
            raise ValueError(
                "No arrival timing available. (You're working too late or it's an interchange)"
            )

        return pendulum.parse(arriving)

    def get_friendly_arrival(self, index=0) -> str:
        try:
            return self.get_arrival(index).diff_for_humans()
        except ValueError:
            return "N/A"

    @property
    def service_code(self) -> str:
        return self.payload["ServiceNo"]

    @property
    def service(self) -> BusService:
        return BusServiceFactory.load_service(self.service_code)

    @property
    def origin(self) -> Stop:
        return StopFactory.load_stop(self.get_next_bus()["OriginCode"])

    @property
    def destination(self) -> Stop:
        return StopFactory.load_stop(self.get_next_bus()["DestinationCode"])

    @property
    def arriving(self) -> pendulum.DateTime:
        return self.get_arrival()

    @property
    def arriving_at(self) -> str:
        return self.get_friendly_arrival()

    def __repr__(self):
        return {
            "is_wab": self.is_wheelchair_accessible(),
            "orign": self.origin,
            "destination": self.destination,
            "arriving": self.arriving,
            "arriving_at": self.arriving_at,
        }


class Arrivals:
    def __init__(self, payload):
        self.payload = payload

    @property
    def bus_stop_code(self) -> str:
        return self.payload["BusStopCode"]

    def all(self) -> List[Arrived]:
        return list(map(Arrived, self.payload["Services"]))

    def get_stop(self) -> Stop:
        return StopFactory.load_stop(self.bus_stop_code)

    def get_service(self, service_number) -> Arrived:
        """
        :param service_number: Bus service number
        :return: Info about the specific service
        """
        service = first_true(
            self.payload["Services"],
            lambda serv: serv["ServiceNo"] == service_number,
        )

        if service is None:
            raise ValueError(f"{service_number} does not exist at that stop!")

        return Arrived(service)


class Datamall:
    def __init__(self):
        self.http = sessions.BaseUrlSession(getenv("DMALL_URL"))

    def bus_arrivals(self, bus_stop_code: str) -> Arrivals:
        response = self.http.get("BusArrivalv2", params={"BusStopCode": bus_stop_code})
        # Let requests raise and exception if status is non-200
        response.raise_for_status()
        return Arrivals(response.json())
