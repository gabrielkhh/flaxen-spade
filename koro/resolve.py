from typing import Dict

from cache import cache
from koro.dataset import JsonLoader


class Stop:
    def __init__(self, stop_data: Dict):
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


class StopFactory:
    @staticmethod
    @cache.memoize()
    def load_stop(bus_stop_code: str) -> Stop:
        read = JsonLoader()
        return Stop(read.load_file("static/stops.json")[bus_stop_code])
