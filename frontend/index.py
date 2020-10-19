from flask import Blueprint, current_app, render_template
from werkzeug.local import LocalProxy

from koro.resolve import BusServiceFactory

logger = LocalProxy(lambda: current_app.logger)

app = Blueprint("frontend", __name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bus/service/<service>")
def bus_service(service):
    service = BusServiceFactory.load_service(service.upper())

    return render_template("bus/service.html", service=service)


@app.route("/bus/stop/<stop>")
def bus_stop(stop):
    pass
