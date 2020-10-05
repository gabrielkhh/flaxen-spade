import click
from flask import Blueprint, current_app

from cache import cache
from koro.geo import resolve_coordinates

cli = Blueprint("flaxen", __name__, cli_group=None)


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
