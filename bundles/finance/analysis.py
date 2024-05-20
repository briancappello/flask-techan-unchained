import pandas as pd
# import pystore
import exchange_calendars as tc
import talib.stream as ta

from datetime import date

"""
analyze in:
    start_date
    symbols
    root_dir
    analyzers_module_name

interface to fetch data given symbol, timeframe, end_date, limit
interface to store results given timeframe + dataframe

filter in:
    start_date
    timeframe_dfs ?

interface to fetch data given timeframe + date
interface to store results given date +
"""

class Analyze:
    analyzers_module_name = 'bundles.finance.analyzers'
    filters_module_name = 'bundles.finance.filters'

    def __init__(self, start_date=None, end_date=None):
        self.nyse: tc.ExchangeCalendar = tc.get_calendar('NYSE')
        self.store = pystore.store('finance')

        today = pd.Timestamp(date.today(), tz='UTC')
        end_date = end_date and pd.Timestamp(end_date, tz='UTC') or (
            today if self.nyse.is_session(today) else self.nyse.previous_close(today)
        )
        start_date = start_date and pd.Timestamp(start_date, tz='UTC') or end_date
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        for day in self.sessions:
            next_session = self.nyse.next_session(day)
            filter_results = self.fetch_collection(f'filters-{day.isoformat()}')
            buys, sells = self.get_trades(filter_results)
            # enter trades at *next* open price

    @property
    def sessions(self):
        return self.nyse.sessions_in_range(self.start_date, self.end_date)

    def fetch(self, collection, name):
        return self.collection(collection).item(name).to_pandas(parse_dates=False)

    def fetch_collection(self, name):
        data = {}
        collection = self.collection(name)
        for item in collection.list_items():
            data[item] = collection.item(item).to_pandas(parse_dates=False)
        return data

    def collection(self, name):
        return self.store.collection(name)


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
    ts = prev_high.name
    return len(df) - df.index.get_loc(ts) - 1


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
