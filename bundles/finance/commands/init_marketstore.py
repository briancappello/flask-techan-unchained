import os
import sys

from flask_unchained.cli import click

from ..services import IndexManager

from .group import finance


HEADER = '''
# -----------------------------------------
# Auto-generated marketstore configuration.
# -----------------------------------------
root_directory: /data     # root directory of the marketstore database
listen_port: 5993         # the port exposed by the database server
log_level: info           # (info|warn|error)
queryable: true
stop_grace_period: 0
wal_rotate_interval: 5
enable_add: true
enable_remove: false
enable_last_known: false
# timezone: "America/New_York"
'''

PREFIX = '        '


@finance.command()
@click.argument('indexes', nargs=-1, required=False,
                help='Which indexes (by symbol) to download data for.')
@click.option('-f', '--filename', nargs=1, required=False,
              help='The filename to output results to (default STDOUT)')
def init_marketstore(indexes, filename):
    index_manager = IndexManager()
    indexes = index_manager.find_by_tickers(indexes)

    lines = []
    for index in indexes:
        lines.append(f'{PREFIX}# {index.name}')
        symbols = sorted(equity.ticker for equity in index.equities)
        for symbol in symbols:
            lines.append(f'{PREFIX}- {symbol}')

    output = '\n'.join(lines)
    if not filename:
        print(output)
        sys.exit(0)

    dirname = os.path.dirname(filename)
    os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as f:
        f.write(output + '\n')
