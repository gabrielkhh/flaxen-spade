from flask import Blueprint, render_template
from cache import cache

app = Blueprint("frontend", __name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cachetest")
@cache.memoize(50)
def xd():
    return "test"
