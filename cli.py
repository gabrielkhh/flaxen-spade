import click
from flask import Blueprint, current_app

from cache import cache

cli = Blueprint("flaxen", __name__, cli_group=None)


@cli.cli.command("clear-cache")
def clear_cache():
    cache.clear()
    click.echo("Cache cleared!")


@cli.cli.command("stats")
@click.option("--file", prompt="Which file?")
def stats(file):
    """Help output here"""
    print(f"Stats for {file}")
    print(current_app.instance_path)
