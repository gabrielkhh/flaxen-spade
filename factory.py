import logging.config
import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from backend.api import api
from cache import cache
from cli import cli, merge, t
from frontend.index import app as frontend

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="JtgKOSZ3fleZu7pDm9hI0Kkf4OnGjVE1l1+hDRecNnU=")

    cache.init_app(app)
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)

    # Mount routes
    app.register_blueprint(frontend, templates="templates")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(cli)
    app.register_blueprint(merge)
    app.register_blueprint(t)

    @app.errorhandler(404)
    def not_found(error):
        return f"404."

    return app
