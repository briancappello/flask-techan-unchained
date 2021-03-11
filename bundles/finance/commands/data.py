import aiohttp
import asyncio
import json
import multiprocessing
import numpy as np
import pandas as pd
import pymarketstore as pymkts
import pystore
import pandas_market_calendars as tc
import talib.stream as ta

from collections import defaultdict
from datetime import date, timezone
from flask_unchained import injectable, unchained
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
    symbols = symbols or []
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
        dl_all(list(set(equities.keys()) | set(symbols)))
    )

    if errors:
        click.echo('!!! Handling Errors !!!')
        for error in errors:
            if isinstance(error, tuple):
                symbol, msg = error
                if msg == 'Not Found':
                    equity_manager.delete(equities[symbol])
                else:
                    print(f'{symbol}: {msg}')
            else:
                print(error)  # FIXME: properly handle exceptions...
        equity_manager.commit()

    click.echo('Done')


def get_df(symbol, timeframe='1D', attrgroup='OHLCV'):
    client = pymkts.Client()
    p = pymkts.Param(symbol, timeframe, attrgroup, start='2015-01-01')
    return client.query(p).first().df()


def prev_higher_bar(df: pd.DataFrame):
    """
    Returns the most recent prior bar with a higher close than the last bar in `df`.
    """
    latest = df.Close.iloc[-1]
    prev_higher_bars = df[df.High >= latest][:-1]
    if not len(prev_higher_bars):
        return None
    return prev_higher_bars.iloc[-1]


def num_bars_since_prev_high(df: pd.DataFrame):
    """
    Counts the number of bars since the prior high.
    """
    prev_high = prev_higher_bar(df)
    if prev_high is None:
        return len(df) - 1
    return len(df) - df.index.get_loc(prev_high.name) - 1


def is_expanding_volume(df: pd.DataFrame, num_bars: int = 3) -> bool:
    if len(df) < num_bars:
        return False
    return (df.index[-num_bars:] == df.Volume[-num_bars:].sort_values().index).all()


def is_expanding_bodies(df: pd.DataFrame, num_bars: int = 3, bullish: bool = True) -> bool:
    bars = df[-num_bars:]
    bodies = bars.Close - bars.Open

    # check all bars are in the same direction
    # allow the first bar to be a doji w/ same open & close
    all_up_days = (bodies >= 0).all()
    all_down_days = (bodies <= 0).all()
    if (bullish and not all_up_days) or (not bullish and not all_down_days):
        return False

    is_advancing = (bars.index == bars.Close.sort_values(ascending=bullish).index).all()
    bodies_expanding = (bars.index == bodies.sort_values(ascending=bullish).index).all()
    return is_advancing and bodies_expanding


def median_volume(df: pd.DataFrame, num_bars: int = 50) -> float:
    if len(df) <= num_bars:
        return float(np.median(df.Volume))
    return float(np.median(df.Volume[-num_bars:]))


def median_body(df: pd.DataFrame, num_bars: int = 50) -> float:
    bodies = (df.Close[-num_bars:] - df.Open[-num_bars:]).abs()
    return float(np.median(bodies))


def volume_multiple_of_median(df: pd.DataFrame, num_bars: int = 50) -> float:
    return df.Volume.iloc[-1] / median_volume(df, num_bars)


def volume_sum_of_prior_days(df: pd.DataFrame) -> int:
    if len(df) < 2 or df.Volume.iloc[-2] > df.Volume.iloc[-1]:
        return 0

    sum = 0
    prior_days = 0
    while len(df) >= (prior_days + 2) and sum < df.Volume.iloc[-1]:
        sum += df.Volume.iloc[-(prior_days + 2)]
        prior_days += 1
    return prior_days


def is_trading_safe(df):
    return len(df) > 3 and median_volume(df) > 200_000


def crossed_ma(df: pd.DataFrame, ma: int = 200, within_bars: int = 1):
    if len(df) < ma:
        return False

    sma = ta.SMA(df.Close, timeperiod=ma)
    for i in range(1, within_bars + 1):
        if df.Open.iloc[-i] < sma < df.Close.iloc[-1]:
            return True
    return False


def gapped_ma(df: pd.DataFrame, ma: int = 200):
    if len(df) < ma:
        return False
    yesterday, today = df.iloc[-2], df.iloc[-1]
    return yesterday.Close < ta.SMA(df.Close, timeperiod=ma) < today.Open


def true_false_counts(series: pd.Series):
    """
    input: a boolean series
    returns: two-tuple (num_true, num_false)
    """
    return series.value_counts().sort_index(ascending=False).tolist()


# FIXME
# crosses
# gaps
# within percent of
# down day, up day w/ higher volume, open gap up on high premarket volume
# bounce off upward-sloping ma (down day closing near ma, up day opening near ma)


@unchained.inject()
def get_data(symbols: Optional[List[str]] = None,
             timeframe: str = '1D',
             limit: int = 200,
             end_date: Optional[str] = None,
             marketstore_service: MarketstoreService = injectable):
    symbols = symbols or marketstore_service.get_symbols()
    data = marketstore_service.get_bulk_history(
        symbols, timeframe, limit=limit, end=end_date)
    for symbol, df in data.items():
        if is_trading_safe(df):
            yield symbol, df


@finance.command('expanding-bodies')
@click.option('--bearish', is_flag=True, required=False, default=False)
@click.option('--date', required=False, type=pd.Timestamp)
def expanding_bodies(bearish=False, date=None):
    symbols = []
    for symbol, df in get_data(limit=250, end_date=date):
        if is_expanding_volume(df) and is_expanding_bodies(df, bullish=not bearish):
            two_days_ago = num_bars_since_prev_high(df[:-2])
            yesterday = num_bars_since_prev_high(df[:-1])
            today = num_bars_since_prev_high(df)
            if today > 100 and yesterday < 10 and two_days_ago < 10:
                symbols.append(symbol)

    with open('/home/brian/expanding-bodies.json', 'w') as f:
        json.dump(symbols, f)


@finance.command('new-highs')
def new_highs():
    symbols = []
    for symbol, df in get_data(limit=300):
        if df.Close.iloc[-1] < df.Open.iloc[-1]:
            continue

        yesterday = num_bars_since_prev_high(df[:-1])
        today = num_bars_since_prev_high(df)
        if yesterday < 5 and today > 250:
            symbols.append(symbol)

    with open('/home/brian/new-highs.json', 'w') as f:
        json.dump(symbols, f)


# FIXME breakout new highs (above also catches new highs in uptrends)


@finance.command('crossed-sma')
@click.option('--sma', type=int, required=False, default=200)
@click.option('--within-bars', type=int, required=False, default=2)
def crossed_sma_high_volume(sma, within_bars):
    symbols = []
    for symbol, df in get_data(limit=sma):
        # if has high volume and recently crossed 200sma
        if crossed_ma(df, ma=sma, within_bars=within_bars) and volume_multiple_of_median(df) > 2:
            symbols.append(symbol)

    with open('/home/brian/crossed-sma.json', 'w') as f:
        json.dump(symbols, f)


@finance.command('high-volume')
def high_volume():
    symbols = []
    for symbol, df in get_data(limit=100):
        if volume_multiple_of_median(df) >= 2 and volume_sum_of_prior_days(df) >= 4:
            symbols.append(symbol)

    with open('/home/brian/high-volume.json', 'w') as f:
        json.dump(symbols, f)


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
        self.nyse: tc.MarketCalendar = tc.get_calendar('NYSE')
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

# FIXME
# watch events, eg:
# if SYMBOL does X (price goes above/below N) then alert me

