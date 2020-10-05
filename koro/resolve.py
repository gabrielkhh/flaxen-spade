from typing import Dict

from cache import cache
from koro.dataset import JsonLoader


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
        return self.stop_code


class StopFactory:
    @staticmethod
    @cache.memoize()
    def load_stop(bus_stop_code: str) -> Stop:
        read = JsonLoader()
        return Stop(bus_stop_code, read.load_file("static/stops.json")[bus_stop_code])
