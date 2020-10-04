from os import getenv

from requests_toolbelt import sessions

from koro.manipulation import first_true


class BusArrival:
    def __init__(self, payload):
        self.payload = payload

    @property
    def bus_stop_code(self):
        return self.payload["BusStopCode"]

    def get_service(self, service_number):
        """
        :param service_number: Bus service number
        :return: Info about the specific service
        """
        return first_true(
            self.payload["Services"],
            lambda service: service["ServiceNo"] == service_number,
        )


class Datamall:
    def __init__(self):
        self.http = sessions.BaseUrlSession(getenv("DMALL_URL"))

    def bus_arrivals(self, bus_stop_code: str) -> BusArrival:
        return BusArrival(
            self.http.get("BusArrivalv2", params={"BusStopCode": bus_stop_code}).json()
        )
