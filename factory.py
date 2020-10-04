import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from backend.api import api
from cache import cache
from cli import cli
from frontend.index import app as frontend


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="JtgKOSZ3fleZu7pDm9hI0Kkf4OnGjVE1l1+hDRecNnU=")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cache.init_app(app)
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)

    # Mount routes
    app.register_blueprint(frontend, templates="templates")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(cli)

    return app
