from flask_unchained import injectable
from flask_unchained.cli import click

from .group import finance
from ..services import DataService, EquityManager, MarketstoreService
from ..vendors import yahoo


@finance.command()
def init():
    data_service = DataService(click.echo)
    data_service.init()


@finance.command()
@click.argument('symbols', nargs=-1)
def sync(
    symbols,
    equity_manager: EquityManager = injectable,
    marketstore_service: MarketstoreService = injectable,
):
    if not symbols:
        symbols = [equity.ticker for equity in equity_manager.all()]

    for i, symbol in enumerate(symbols):
        click.echo(f'{i+1}/{len(symbols)}: Syncing data for {symbol}')

        df = yahoo.get_daily_df(symbol)
        if df is None:
            print(f'no data for {symbol}')
            continue

        resp = marketstore_service.write(df, f'{symbol}/1D/OHLCV')
        if resp['responses'] is not None:
            print(resp)

    click.echo('Done.')
