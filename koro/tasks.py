import re
from typing import Optional

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
            Task(
                "Shopping Mall Passenger Volume", "shopping-mall-passenger-volume.json"
            ),
        ]

    def find_task(self, slug) -> Optional[Task]:
        return first_true(self.tasks, lambda task: task.slug == slug)

    def get_tasks(self):
        return self.tasks
