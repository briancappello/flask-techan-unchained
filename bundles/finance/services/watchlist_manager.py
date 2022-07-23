import pandas as pd

from flask_unchained import injectable
from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Watchlist
from ..vendors import yahoo
from .data_service import DataService
from .historical_signals_service import HistoricalSignalsService


class WatchlistManager(ModelManager):
    data_service: DataService = injectable
    config = injectable
    historical_signals_service: HistoricalSignalsService = injectable

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
        elif key == 'gainers':
            tickers = yahoo.get_gainers_tickers().index
        elif key == 'losers':
            tickers = yahoo.get_losers_tickers().index

        if not len(tickers):
            if key not in self.historical_signals_service.signal_names:
                raise RuntimeError(f'Watchlist(key={key}) not found')

            watchlists = self.historical_signals_service.get_by_date()
            tickers = watchlists[key]

        return dict(key=key, components=self.data_service.get_quotes(tickers=tickers))

    def get_most_actives(self):
        return self.data_service.get_quotes(yahoo.get_most_actives().index)

    def get_trending(self):
        return self.data_service.get_quotes(yahoo.get_trending_tickers().index)

    def get_gainers(self):
        return self.data_service.get_quotes(yahoo.get_gainers_tickers().index)

    def get_losers(self):
        return self.data_service.get_quotes(yahoo.get_losers_tickers().index)


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
