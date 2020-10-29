import re
from typing import Optional

from flask import render_template, request

from koro.dataset import JsonLoader
from koro.manipulation import first_true


class Task:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.slug = self.slugify(name)

    def slugify(self, name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


class TaskBuilder:
    def __init__(self):
        self.tasks = [
            Task("Best time to travel", "best_time_to_travel.json"),
            Task(
                "Popular MRT routes on weekends",
                "pop_mrt_routes_on_weekends_publicholiday.json",
            ),
            Task("Popular End Trips", "popular_end_trip.json"),
            Task("Popular Stations", "popular_stations.json"),
        ]

    def find_task(self, slug) -> Optional[Task]:
        return first_true(self.tasks, lambda task: task.slug == slug)

    def get_tasks(self):
        return self.tasks


class ViewDispatcher:
    def __init__(self):
        self.dispatch_table = {
            "best-time-to-travel": self.best_time_to_travel,
            "popular-mrt-routes-on-weekends": self.popular_mrt_routes_on_weekends,
            "popular-end-trips": self.popular_end_trips,
            "popular-stations": self.popular_stations,
        }

    def dispatch(self, slug):
        return self.dispatch_table[slug]()

    def best_time_to_travel(self):
        results = JsonLoader().load_file("results/best_time_to_travel.json")

        if filter_by := request.args.get("filter"):
            results = {
                key: value for key, value in results.items() if filter_by.upper() in key
            }

        return render_template("tasks/best_time.html", results=results)

    def popular_mrt_routes_on_weekends(self):
        results = JsonLoader().load_file(
            "results/pop_mrt_routes_on_weekends_publicholiday.json"
        )

        if filter_by := request.args.get("filter"):
            results = {
                key: value for key, value in results.items() if filter_by.upper() in key
            }

        return render_template("tasks/popular_mrt_routes.html", results=results)

    def popular_end_trips(self):
        results = JsonLoader().load_file("results/popular_end_trip.json")

        if filter_by := request.args.get("filter"):
            new = {}
            for month in ["06", "07", "08"]:
                new["month"] = {
                    key: value
                    for key, value in results[month].items()
                    if filter_by.upper() in key
                }

            results = new

        return render_template("tasks/popular_end_trips.html", results=results.items())

    def popular_stations(self):
        results = JsonLoader().load_file("results/popular_stations.json")

        if filter_by := request.args.get("filter"):
            new = {}
            for key, stations in results.items():
                new[key] = [
                    station
                    for station in stations
                    if filter_by in station["station_name"].lower()
                ]

            results = new

        return render_template("tasks/popular_stations.html", results=results)
