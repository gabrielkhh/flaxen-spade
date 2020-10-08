from flask import Blueprint, current_app, render_template
from werkzeug.local import LocalProxy

from koro.dataset import JsonLoader
from koro.resolve import BusServiceFactory

logger = LocalProxy(lambda: current_app.logger)

app = Blueprint("frontend", __name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/bus/<service>")
def bus_service(service):
    service = BusServiceFactory.load_service(service.upper())

    return render_template("services.html", service=service)
