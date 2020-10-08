import json
from typing import Dict

import polyline

from cache import cache
from koro.dataset import CsvLoader, JsonLoader
from koro.manipulation import first_true


class Stop:
    def __init__(self, stop_code: str, stop_data: Dict):
        self.stop_code = stop_code
        self.stop_data = stop_data

    @property
    def name(self):
        return self.stop_data["name"]

    @property
    def latitude(self):
        return self.stop_data["lat"]

    @property
    def longitude(self):
        return self.stop_data["lng"]

    def __repr__(self) -> str:
        return json.dumps(self.stop_data)


class StopFactory:
    @staticmethod
    @cache.memoize()
    def load_stop(bus_stop_code: str) -> Stop:
        read = JsonLoader()
        return Stop(bus_stop_code, read.load_file("static/stops.json")[bus_stop_code])


class BusService:
    def __init__(self, bus_service_code, service_data):
        self.bus_service_code = bus_service_code
        self.service_data = service_data
        self.resolved_stops = []
        self.resolved_stop_coordinates = []

    def resolve_stops(self):
        # 1 or 2 routes
        for route in self.service_data:
            self.resolved_stops.append([self.get_stop(stop) for stop in route])

    def resolve_routes(self):
        for route in self.stops:
            self.resolved_stop_coordinates.append([
                (stop['lat'], stop['lng']) for stop in route
            ])

    def get_stop(self, bus_stop_code) -> Dict:
        return StopFactory.load_stop(bus_stop_code).stop_data

    @property
    def stops(self):
        if self.resolved_stops:
            return self.resolved_stops

        self.resolve_stops()
        return self.resolved_stops

    @property
    def points(self):
        # Use stored attr on subsequent calls
        if self.resolved_stop_coordinates:
            return self.resolved_stop_coordinates

        self.resolve_routes()
        return self.resolved_stop_coordinates

    @property
    def polyline(self):
        try:
            loaded = JsonLoader().load_file(f"static/routes/mytransportsg/{self.bus_service_code}.json")[0]
        except FileNotFoundError:
            try:
                loaded = JsonLoader().load_file(f"static/routes/onemapsg/{self.bus_service_code}.json")[0]
            except FileNotFoundError as e:
                raise e

        return list(map(lambda point: [point[1], point[0]], loaded))


class BusServiceFactory:
    @staticmethod
    @cache.memoize()
    def load_service(bus_service_code: str) -> BusService:
        return BusService(
            bus_service_code,
            JsonLoader().load_file("static/serviceStops.json")[bus_service_code],
        )


class TrainStation:
    def __init__(self, payload):
        self.code = payload["station_code"]
        self.name = payload["mrt_station"]
        self.line = payload["mrt_line"]
        self.latitude = payload["lat"]
        self.longitude = payload["long"]


class TrainStationFactory:
    @staticmethod
    @cache.memoize()
    def load_station(station_code: str) -> TrainStation:
        stations = CsvLoader().load_file("merged/train-data.csv")
        found_station = first_true(
            stations,
            lambda station: station["station_code"] == station_code.upper(),
        )

        if found_station is None:
            raise ValueError(f"{station_code} does not exist!")

        return TrainStation(found_station)
