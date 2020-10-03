import click
from flask import Blueprint, current_app

cli = Blueprint("flaxen", __name__, cli_group=None)


@cli.cli.command("stats")
@click.option('--file', prompt='Which file?')
def stats(file):
    """Help output here"""
    print(f"Stats for {file}")
    print(current_app.instance_path)
