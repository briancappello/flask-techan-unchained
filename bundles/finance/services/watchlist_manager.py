import json
import pandas as pd
import numpy as np

from typing import *

from flask_unchained import Service, injectable
from flask_unchained.bundles.sqlalchemy import ModelManager
from flask_unchained.string_utils import kebab_case

from .. import analysis
from ..models import Watchlist
from ..vendors import yahoo
from .data_service import DataService
from .marketstore_service import MarketstoreService


class WatchlistManager(ModelManager):
    data_service: DataService = injectable
    config = injectable

    class Meta:
        model = Watchlist

    def create(self, commit: bool = False, **kwargs) -> Watchlist:
        return super().create(commit=commit, **kwargs)

    def find_by_user(self, user):
        return self.q.filter_by(user_id=user.id)

    def get_watchlist(self, key):
        tickers = []
        if key == 'most-actives':
            tickers = yahoo.get_most_actives().index
        elif key == 'trending':
            tickers = yahoo.get_trending_tickers().index

        if not len(tickers):
            if key not in {'crossed-sma', 'high-volume', 'expanding-bodies', 'new-highs'}:
                raise RuntimeError(f'Watchlist(key={key}) not found')

            with open(f'/home/brian/{key}.json') as f:
                tickers = json.load(f)

        return dict(key=key, components=self.data_service.get_quotes(tickers=tickers))

    def get_most_actives(self):
        return self.data_service.get_quotes(yahoo.get_most_actives().index)

    def get_trending(self):
        return self.data_service.get_quotes(yahoo.get_trending_tickers().index)


def watchlist(fn):
    setattr(fn, '__watchlist__', kebab_case(fn.__name__))
    return fn


class OpportunityFinder(Service):
    marketstore_service: MarketstoreService = injectable

    def run(self):
        data = list(self._get_data(limit=300))

    def _get_data(self,
                  symbols: Optional[List[str]] = None,
                  timeframe: str = '1D',
                  limit: int = 200,
                  ):
        symbols = symbols or self.marketstore_service.get_symbols()
        data = self.marketstore_service.get_bulk_history(symbols, timeframe, limit=limit)
        for symbol, df in data.items():
            if analysis.is_trading_safe(df):
                yield symbol, df

    @watchlist
    def crossed_sma(self, data):
        pass

    @watchlist
    def high_volume(self, data):
        pass

    @watchlist
    def expanding_bodies(self, data):
        pass

    @watchlist
    def new_highs(self, data):
        pass


def find_it(df, date=None):
    dti = get_day_index_from_minutes(df)
    if date:
        today = pd.Timestamp(date, tz='America/New_York')
    else:
        today = dti[-1]
    yesterday = dti[dti.get_loc(today)-1]
    median_volume = df[f'{yesterday} 09:30':f'{yesterday} 16:00'].Volume.median()

    for ts, bar in df[today.date().isoformat()].iterrows():
        if is_moving_big(bar, median_volume):
            return ts


def is_moving_big(bar, yesterdays_intraday_median_volume):
    volume_multiple = bar.Volume / yesterdays_intraday_median_volume
    pct_change = (bar.Close - bar.Open) / bar.Open

    return (
        volume_multiple > 8
        and
        0.08 < pct_change < max(0.2, volume_multiple / 200)
    )


def get_next_bar(df, ts):
    return df.iloc[df.index.get_loc(ts) + 1]


def get_max_gain_bar(df, signal_ts):
    next_bar = get_next_bar(df, signal_ts)
    entry = (next_bar.Open + next_bar.Close) / 2
    gains = df[next_bar.name:].Close - entry
    best_ts = gains.sort_values(ascending=False).index[0]
    return df.loc[best_ts]


def get_day_index_from_minutes(df):
    idf = pd.DataFrame(range(len(df)), index=df.index)
    return idf.resample('1D').mean().dropna().index
