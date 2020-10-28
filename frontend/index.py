from flask import Blueprint, abort, current_app, render_template
from requests import HTTPError
from werkzeug.local import LocalProxy

from cache import cache
from koro.datamall import Datamall
from koro.dataset import JsonLoader
from koro.manipulation import dataset_path, directory_size
from koro.resolve import BusServiceFactory, StopFactory
from koro.tasks import TaskBuilder, ViewDispatcher

logger = LocalProxy(lambda: current_app.logger)

app = Blueprint("frontend", __name__)


@app.route("/")
def index():
    sizes = {}
    for directory in ["large", "merged", "od", "raw_other", "results", "static"]:
        sizes[directory] = directory_size(dataset_path(directory))

    return render_template("index.html", sizes=sizes)


@app.route("/buses")
def service_index():
    services = JsonLoader().load_file("static/services.final.json").items()
    services = [{"name": service["name"], "code": code} for code, service in services]

    return render_template("bus/bus_index.html", buses=services)


@app.route("/stops")
def stop_index():
    stops = StopFactory.all()
    stops = [
        {
            "name": stop.name,
            "code": stop.stop_code,
            "lat": stop.latitude,
            "lng": stop.longitude,
        }
        for stop in stops
    ]
    return render_template("bus/stop_index.html", stops=stops)


@app.route("/bus/service/<service>")
@cache.cached(timeout=30)
def bus_service(service):
    try:
        service = BusServiceFactory.load_service(service.upper())
    except KeyError:
        abort(404)

    return render_template("bus/service.html", service=service)


@app.route("/bus/stop/<stop>")
@cache.cached(timeout=30)
def bus_stop(stop):
    try:
        stop = Datamall().bus_arrivals(stop)
    except HTTPError as e:
        abort(404)

    return render_template("bus/stop.html", stop=stop.get_stop(), services=stop.all())


@app.route("/task")
def all_tasks():
    return render_template("tasks/index.html", tasks=TaskBuilder().get_tasks())


@app.route("/task/<slug>")
def available_tasks(slug):
    return ViewDispatcher().dispatch(slug)
