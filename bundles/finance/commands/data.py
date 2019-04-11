from flask_unchained.cli import click

from .group import finance
from ..services import DataService


@finance.command()
def init():
    data_service = DataService(click.echo)
    data_service.init()
