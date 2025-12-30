import os
import json

from sqlalchemy import cast, Integer

from fin_models.config import Config as FinModelsConfig
from fin_models.enums import Freq
from fin_models.services import nyse
from fin_models.vendors import yahoo
from flask_unchained import injectable
from flask_unchained.bundles.sqlalchemy import ModelManager, SessionManager

from ..models import Watchlist, Stats
from .data_service import DataService



class WatchlistManager(ModelManager):
    data_service: DataService = injectable
    session_manager: SessionManager = injectable
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
            tickers = self._get_watchlist_symbols_from_stats('bar_volume')
        elif key == 'gainers':
            tickers = self._get_watchlist_symbols_from_stats('percent_change')
        elif key == 'trending':
            tickers = self._get_watchlist_symbols_from_stats('volume_multiple_of_median')
        elif key == 'expanding-bbands':
            tickers = self._get_watchlist_symbols_from_stats_bool('is_expanding_bbands')

        if not len(tickers):
            wl_dir = os.path.join(FinModelsConfig.DATA_DIR, 'watchlists')
            wl_path = os.path.join(wl_dir, f'{key}.json')
            if os.path.exists(wl_path):
                with open(wl_path) as f:
                    data = json.load(f)
                    tickers = data.get('tickers', [])

            elif key not in {'crossed-sma', 'high-volume', 'expanding-bodies', 'new-highs'}:
                raise RuntimeError(f'Watchlist(key={key}) not found')
            else:
                with open(f'/home/brian/{key}.json') as f:
                    tickers = json.load(f)

        return dict(key=key, components=self.data_service.get_quotes(tickers=tickers))

    def get_most_actives(self):
        return self.data_service.get_quotes(yahoo.get_most_actives().index)

    def get_trending(self):
        return self.data_service.get_quotes(yahoo.get_trending_tickers().index)

    def _get_latest_stats_day(self, freq: Freq = Freq.day):
        latest = self.session_manager.query(Stats).filter_by(freq=freq).order_by(Stats.day.desc()).limit(1).one_or_none()
        if latest is not None:
            print(f'using stats for day {latest.day}')
            return latest.day
        return nyse.get_latest_trading_date()

    def _get_watchlist_symbols_from_stats(self, key: str) -> list[str]:
        return [
            row.symbol
            for row in self.session_manager.query(Stats)
            .filter(Stats.day == self._get_latest_stats_day(),
                    Stats.stats.has_key(key),
                    cast(Stats.stats['median_volume'], Integer) > 50_000)
            .order_by(Stats.stats[key].desc())
            .limit(50)
            .all()
        ]

    def _get_watchlist_symbols_from_stats_bool(self, key: str) -> list[str]:
        return [
            row.symbol
            for row in self.session_manager.query(Stats)
            .filter(Stats.day == self._get_latest_stats_day(),
                    Stats.stats.has_key(key),
                    cast(Stats.stats['median_volume'], Integer) > 50_000)
            .order_by(Stats.stats['median_volume'].desc())
            .limit(50)
            .all()
        ]
