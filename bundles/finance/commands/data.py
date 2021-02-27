import aiohttp
import asyncio
import multiprocessing
import numpy as np
import pandas as pd
import pymarketstore as pymkts
import pystore
import trading_calendars as tc

from collections import defaultdict
from datetime import date, timezone
from flask_unchained import unchained, injectable
from flask_unchained.cli import click
from typing import *

from .group import finance
from ..analyzers import AnalyzersRunner
from ..filters import FiltersRunner
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
            df = yahoo.yfi_json_to_df(data, '1d')
            if df is None:
                return symbol, "Invalid Data"
            click.echo(f'writing {symbol}')
            marketstore_service.write(df, f'{symbol}/1D/OHLCV')

    async def dl_all(symbols):
        errors = []
        async with aiohttp.ClientSession() as session:
            for batch in chunk(symbols, 8):
                tasks = [dl(session, symbol) for symbol in batch]
                results = await asyncio.gather(*tasks, return_exceptions=False)
                errors.extend([error for error in results if error])
        return errors

    loop = asyncio.get_event_loop()
    errors = loop.run_until_complete(
        dl_all(list(equities.keys()))
    )

    if errors:
        click.echo('!!! Handling Errors !!!')
        for error in errors:
            if isinstance(error, tuple):
                symbol, msg = error
                if msg == 'Not Found':
                    equity_manager.delete(equities[symbol])
            else:
                print(error)  # FIXME: properly handle exceptions...
        equity_manager.commit()

    click.echo('Done')


def get_df(symbol, timeframe='1D', attrgroup='OHLCV'):
    client = pymkts.Client()
    p = pymkts.Param(symbol, timeframe, attrgroup, start='2015-01-01')
    return client.query(p).first().df()


def analyze_symbol(symbol):
    df = get_df(symbol, '1D')
    if df is None or not len(df):
        return None

    median = np.median(df.Volume)
    return dict(symbol=symbol, median=median)


@finance.command()
def clean(marketstore_service: MarketstoreService = injectable):
    symbols = marketstore_service.get_symbols()
    for symbol in symbols:
        if len(symbol) > 4 or not symbol.isupper():
            print('cleaning ', symbol)
            marketstore_service.client.destroy(f'{symbol}/1Min/OHLCV')
            marketstore_service.client.destroy(f'{symbol}/1D/OHLCV')


@finance.command()
@click.option('--start', default=None)
@click.option('--end', default=None)
def analyze(start=None, end=None):
    analyzer = Analyze(start, end)
    analyzer.run()


@finance.command()
@click.option('--start', default=None)
@click.option('--end', default=None)
def show(start=None, end=None):
    analyzer = Analyze(start, end)
    analyzer.show()


@unchained.inject()
class Analyze:
    analyzers_module_name = 'bundles.finance.analyzers'
    filters_module_name = 'bundles.finance.filters'

    marketstore_service: MarketstoreService = injectable

    def __init__(self, start_date=None, end_date=None):
        self.nyse: tc.TradingCalendar = tc.get_calendar('NYSE')
        self.store = pystore.store('finance')

        today = pd.Timestamp(date.today(), tz='UTC')
        end_date = end_date and pd.Timestamp(end_date, tz='UTC') or (
            today if self.nyse.is_session(today) else self.nyse.previous_close(today)
        )
        start_date = start_date and pd.Timestamp(start_date, tz='UTC') or end_date
        self.start_date = start_date
        self.end_date = end_date

    @property
    def sessions(self):
        return self.nyse.sessions_in_range(self.start_date, self.end_date)

    def show(self):
        for day in self.sessions:
            timeframes = self.collection(f'analysis-{day.isoformat()}').list_items()
            print(timeframes)

            filters = self.collection(f'filters-{day.isoformat()}').list_items()
            print(filters)

    def run(self):
        symbols = self.marketstore_service.get_symbols()

        for day in self.sessions:
            print(day.isoformat())

            timeframe_dfs = self.run_analyzers(symbols, day)
            for tf, df in timeframe_dfs.items():
                self.persist(f'analysis-{day.isoformat()}', name=tf, data=df)

            # FIXME allow re-running filters using the cached timeframe_dfs
            filter_results = self.run_opportunity_filters(timeframe_dfs)
            for filter, df in filter_results.items():
                self.persist(f'filters-{day.isoformat()}', name=filter, data=df)
                print(filter, df)

    def run_filters(self):
        for day in self.sessions:
            timeframe_dfs = {}
            for tf in self.collection(f'analysis-{day.isoformat()}').list_items():
                timeframe_dfs[tf] = self.fetch(f'analysis-{day.isoformat()}', tf)

            filter_results = self.run_opportunity_filters(timeframe_dfs)
            for filter, df in filter_results.items():
                self.persist(f'filters-{day.isoformat()}', name=filter, data=df)

    def run_analyzers(self, symbols: List[str], day) -> Dict[str, pd.DataFrame]:
        analyzers_runner = AnalyzersRunner(self.analyzers_module_name, day)

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            analyzer_results = pool.map(analyzers_runner.run, symbols)

        data = defaultdict(list)
        for result in analyzer_results:
            for timeframe, d in result.items():
                data[timeframe].append(d)

        timeframe_dfs = dict()
        for timeframe, rows in data.items():
            timeframe_dfs[timeframe] = pd.DataFrame.from_records(rows, index='symbol')
        return timeframe_dfs

    def run_opportunity_filters(self, timeframe_dfs: Dict[str, pd.DataFrame]):
        filter_runners = FiltersRunner(self.filters_module_name)
        return filter_runners.run(timeframe_dfs)

    def persist(self, collection, name, data, metadata=None):
        metadata = metadata or {}
        self.collection(collection).write(name, data, metadata=metadata, overwrite=True)

    def fetch(self, collection, name):
        return self.collection(collection).item(name).to_pandas(parse_dates=False)

    def has(self, collection, name):
        collection = self.store.collection(collection)
        return name in self.collection(collection).list_items()

    def collection(self, name):
        return self.store.collection(name)
