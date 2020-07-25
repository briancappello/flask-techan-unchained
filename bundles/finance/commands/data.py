import asyncio
import aiohttp

from flask_unchained import injectable
from flask_unchained.cli import click

from .group import finance
from ..services import DataService, EquityManager, MarketstoreService
from ..vendors import yahoo


def chunk(string, size):
    for i in range(0, len(string), size):
        yield string[i:i+size]


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
        equities = {equity.ticker: equity
                    for equity in equity_manager.all()}
    else:
        equities = {equity.ticker: equity
                    for equity in equity_manager.filter_by_tickers(symbols)}

    async def dl(session, symbol):
        url = yahoo.get_yfi_url(symbol)
        try:
            async with session.get(url) as r:
                data = await r.json()
                if r.status != 200:
                    return symbol, data['chart']['error']['code']
        except Exception as e:
            return symbol, e
        else:
            df = yahoo.yfi_json_to_df(data)
            if df is None:
                return symbol, "Invalid Data"
            click.echo(f'writing {symbol}')
            marketstore_service.write(df, f'{symbol}/1D/OHLCV')

    async def dl_all(symbols):
        errors = []
        async with aiohttp.ClientSession() as session:
            for batch in chunk(symbols, 8):
                tasks = [dl(session, symbol) for symbol in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                errors.extend([error for error in results if error])
        return errors

    loop = asyncio.get_event_loop()
    errors = loop.run_until_complete(
        dl_all(list(equities.keys()))
    )

    click.echo('!!! Handling Errors !!!')
    for error in errors:
        if isinstance(error, tuple):
            symbol, msg = error
            if msg == 'Not Found':
                equity_manager.delete(equities[symbol])
        else:
            print(error)
    equity_manager.commit()

    click.echo('Done')






