import click
from flask import Blueprint

cli = Blueprint("flaxen", __name__)


@cli.cli.command("stats")
@click.argument("file")
def stats(file):
    """Help output here"""
    print(f"Stats for {file}")
