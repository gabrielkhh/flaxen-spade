import click
from flask import Blueprint, current_app

from cache import cache
from koro.geo import resolve_coordinates

cli = Blueprint("flaxen", __name__, cli_group=None)
merge = Blueprint("flaxen-merge", __name__, cli_group="merge")
t = Blueprint("flaxen-tasks", __name__, cli_group="task")


@cli.cli.command("clear-cache")
def clear_cache():
    """Clears the cache"""
    with current_app.app_context():
        cache.clear()
    click.echo("Cache cleared!")


@cli.cli.command("geocoord")
@click.option("--location", prompt="Location")
def geocoord(location):
    """Resolve a coordinate based on a location name"""
    print(resolve_coordinates(location))


@merge.cli.command("train-geo")
def merge_train():
    """Merges train-station.csv and rails.geojson to get train geo data."""
    from commandbus.merge_train import run

    run()
    click.echo("If you see BP14 missing, it is now defunct.")


@t.cli.command("mall-traffic")
def compute_mall_traffic():
    """Outputs volume of people entering various shopping malls by using data from MRT stations that are in near proximity to a shopping mall."""
    from commandbus.shopping_mall_traffic import mall_traffic

    mall_traffic()


@t.cli.command("best-time-travel")
def best_travel_times():
    from commandbus.best_time_to_travel import run

    run()


@t.cli.command("pop-mrt")
def pop_mrt():
    from commandbus.pop_mrt_routes_on_weekends import run

    run()


@click.option("--count", prompt="Enter value")
@t.cli.command("popular-stations")
def popular_station(count):
    """Shows top x MRT Stations during Weekday Peak Hours"""
    from commandbus.popular_stations_peak_hour import run

    run(count)


@t.cli.command("pop-end-trip")
def pop_end_trip():
    """Popular End Trip"""
    from commandbus.popular_end_trip import end_trip

    end_trip()
