import json
import os

from flask_unchained import injectable
from flask_unchained.cli import click

from ..services.historical_signals_service import HistoricalSignalsService

from .group import finance


@finance.command()
@click.option('--date', type=str, required=False)
def analyze(date=None,
            config=injectable,
            historical_signals_service: HistoricalSignalsService = injectable):
    """
    Run signals analysis and store to disk as JSON.
    """
    results = historical_signals_service.run(end_date=date)
    date = results['date']
    filepath = os.path.join(config.APP_DATA_FOLDER, 'signals', f'{date}.json')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(results['results'], f, indent=4)
    click.echo(f'Results saved to {filepath}')


"""
FIXME
-----

read signals, report P&L stats over next N days

"""
