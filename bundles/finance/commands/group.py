from flask_unchained.cli import cli


@cli.group()
def finance():
    """Finance bundle commands."""
