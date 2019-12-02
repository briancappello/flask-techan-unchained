from flask_unchained import injectable
from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Watchlist
from ..vendors.yahoo import get_most_actives, get_trending_tickers
from .data_service import DataService


class WatchlistManager(ModelManager):
    data_service: DataService = injectable

    class Meta:
        model = Watchlist

    def create(self, commit: bool = False, **kwargs) -> Watchlist:
        return super().create(commit=commit, **kwargs)

    def find_by_user(self, user):
        return self.q.filter_by(user_id=user.id)

    def get_most_actives(self):
        ma = get_most_actives()
        return self.data_service.get_quotes(ma.index)

    def get_trending(self):
        trending = get_trending_tickers()
        return self.data_service.get_quotes(trending.index)
