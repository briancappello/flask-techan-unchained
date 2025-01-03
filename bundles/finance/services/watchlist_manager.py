import json

from fin_models.vendors import yahoo
from flask_unchained import injectable
from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Watchlist
from ..services import IndexManager
from .data_service import DataService


class WatchlistManager(ModelManager):
    data_service: DataService = injectable
    index_manager: IndexManager = injectable
    config = injectable

    class Meta:
        model = Watchlist

    def create(self, commit: bool = False, **kwargs) -> Watchlist:
        return super().create(commit=commit, **kwargs)

    def find_by_user(self, user):
        return self.q.filter_by(user_id=user.id)

    def get_watchlist(self, key):
        with open(self.config.JSON_WATCHLISTS_PATH) as f:
            json_watchlists: dict = json.load(f)

        if key in json_watchlists:
            return dict(
                key=key,
                components=self.data_service.get_quotes(
                    tickers=json_watchlists[key]['tickers'],
                )
            )

        index = self.index_manager.get_by(ticker=key)
        if index is None:
            return dict(key=key, components=[])

        return dict(
            key=index.ticker,
            components=self.data_service.get_quotes(
                tickers=[equity.ticker for equity in index.equities]
            )
        )

        tickers = []

        if key == 'most-actives':
            tickers = yahoo.get_most_actives().index
        elif key == 'trending':
            tickers = yahoo.get_trending_tickers().index

        if not len(tickers):
            if key not in {'crossed-sma', 'high-volume', 'expanding-bodies', 'new-highs'}:
                raise RuntimeError(f'Watchlist(key={key}) not found')

        return dict(key=key, components=self.data_service.get_quotes(tickers=tickers))

    def get_most_actives(self):
        return self.data_service.get_quotes(yahoo.get_most_actives().index)

    def get_trending(self):
        return self.data_service.get_quotes(yahoo.get_trending_tickers().index)
