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
    cache.clear()
    click.echo("Cache cleared!")


@cli.cli.command("geocoord")
@click.option("--location", prompt="Location")
def geocoord(location):
    """Resolve a coordinate based on a location name"""
    print(resolve_coordinates(location))


@cli.cli.command("stats")
@click.option("--file", prompt="Which file?")
def stats(file):
    """Help output here"""
    print(f"Stats for {file}")
    print(current_app.instance_path)


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

@t.cli.command("testcommand")
def my_test_command():
    """My task description"""
    from commandbus import my_first_task
    my_first_task.run()

@t.cli.command("totaltapout")
def total_tap_out():
    """Shows you total tap out count"""
    from commandbus.some_testing import run_test
    run_test()

@t.cli.command("popMrt")
def pop_Mrt():
    from commandbus.pop_Mrt_routes_on_weekends_publicholiday import run
    run()
    

