import click
from flask.cli import with_appcontext

from url_shortener import db


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create database tables."""
    db.create_all()
