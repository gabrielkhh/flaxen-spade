import jsonpickle
from flask import Blueprint, Response, abort, current_app, jsonify, render_template
from requests import HTTPError
from werkzeug.local import LocalProxy

from cache import cache
from koro.datamall import Datamall
from koro.manipulation import dataset_path, directory_size
from koro.resolve import BusServiceFactory

logger = LocalProxy(lambda: current_app.logger)

app = Blueprint("frontend", __name__)


@app.route("/")
def index():
    sizes = {}
    for directory in ["large", "merged", "od", "raw_other", "results", "static"]:
        sizes[directory] = directory_size(dataset_path(directory))

    return render_template("index.html", sizes=sizes)


@app.route("/bus")
def bus_index():
    return render_template("bus/index.html")


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
