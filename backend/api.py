from flask import Blueprint

from koro.dataset import JsonLoader

api = Blueprint("api", __name__)


@api.route("/stop/<stop>")
def api_stop(stop):
    return JsonLoader().load_file("static/routes.lta.json")[stop]
