import jsonpickle
from flask import Blueprint, Response, abort, current_app, jsonify, render_template
from requests import HTTPError
from werkzeug.local import LocalProxy

from koro.datamall import Datamall
from koro.resolve import BusServiceFactory

logger = LocalProxy(lambda: current_app.logger)

app = Blueprint("frontend", __name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bus")
def bus_index():
    return render_template("bus/index.html")


@app.route("/bus/service/<service>")
def bus_service(service):
    try:
        service = BusServiceFactory.load_service(service.upper())
    except KeyError:
        abort(404)

    return render_template("bus/service.html", service=service)


@app.route("/bus/stop/<stop>")
def bus_stop(stop):
    try:
        stop = Datamall().bus_arrivals(stop)
    except HTTPError as e:
        abort(404)

    return render_template("bus/stop.html", stop=stop.get_stop(), services=stop.all())
