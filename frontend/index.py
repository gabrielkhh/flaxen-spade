from flask import Blueprint, abort, current_app, render_template, send_file
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


@app.route("/mall")
def mall_index():
    malls_coordinates = JsonLoader().load_file("static/mallCoordinates.json")
    mall_list = []

    for mall_name, coordinates in malls_coordinates.items():
        mall_name_obj = {"name": mall_name}
        mall_list.append(mall_name_obj)

    return render_template("mall/index.html", malls=mall_list)


@app.route("/mall/<mallName>")
def mall_traffic(mallName):
    mall_traffic_data = JsonLoader().load_file(
        "results/shopping-mall-passenger-volume.json"
    )
    mall = mall_traffic_data["June"][mallName]
    obj_arr_weekday = []
    obj_arr_weekend = []
    fixed_tuple = (
        0,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
    )

    for (counter, data) in enumerate(mall["weekday"]):
        obj_dict = {"hour": fixed_tuple[counter], "volume": data}
        obj_arr_weekday.append(obj_dict)

    for (counter, data) in enumerate(mall["weekends"]):
        obj_dict = {"hour": fixed_tuple[counter], "volume": data}
        obj_arr_weekend.append(obj_dict)

    max_weekday = max(mall["weekday"])
    max_weekend = max(mall["weekends"])
    max_weekday_dict = {
        "hour": fixed_tuple[mall["weekday"].index(max_weekday)],
        "volume": max_weekday,
    }
    max_weekend_dict = {
        "hour": fixed_tuple[mall["weekends"].index(max_weekend)],
        "volume": max_weekend,
    }
    occurrence_dict = {"maxWeekday": max_weekday_dict, "maxWeekend": max_weekend_dict}

    combined_objdict = {"weekday": obj_arr_weekday, "weekend": obj_arr_weekend}

    return render_template(
        "mall/information.html",
        mall=mall,
        mallName=mallName,
        mallObj=combined_objdict,
        occurence=occurrence_dict,
    )


@app.route("/task")
def all_tasks():
    return render_template("tasks/index.html", tasks=TaskBuilder().get_tasks())


@app.route("/task/<slug>")
def available_tasks(slug):
    return ViewDispatcher().dispatch(slug)


@app.route("/export/<slug>")
def available_task_export(slug):
    task = TaskBuilder().find_task(slug)

    return send_file(
        dataset_path(f"results/{task.filename}"),
        mimetype="application/octet-stream",
        as_attachment=True,
    )
