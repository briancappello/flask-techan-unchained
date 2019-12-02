from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Watchlist


class WatchlistManager(ModelManager):
    class Meta:
        model = Watchlist

    def create(self, commit: bool = False, **kwargs) -> Watchlist:
        return super().create(commit=commit, **kwargs)

    def find_by_user(self, user):
        return self.q.filter_by(user_id=user.id)
