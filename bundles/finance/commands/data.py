from flask_unchained import injectable
from flask_unchained.cli import click

from .group import finance
from ..services import DataService, IndexManager, MarketstoreService
from ..vendors import yahoo


@finance.command()
def init():
    data_service = DataService(click.echo)
    data_service.init()


@finance.command()
@click.argument('symbols', nargs=-1)
def sync(
    symbols,
    index_manager: IndexManager = injectable,
    marketstore_service: MarketstoreService = injectable,
):
    if not symbols:
        indexes = index_manager.find_by_tickers(['^DJI', '^DJT', '^DJU', '^NDX', '^SP500'])
        symbols = list(set(
            equity.ticker
            for index in indexes
            for equity in index.equities
        ))

    for i, symbol in enumerate(symbols):
        click.echo(f'{i+1}/{len(symbols)}: Syncing data for {symbol}')
        df = yahoo.get_daily_df(symbol)
        if df is not None:
            resp = marketstore_service.write(df, f'{symbol}/1D/OHLCV')
            if resp['responses'] is not None:
                print(resp)
    click.echo('Done.')
