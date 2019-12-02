from flask_unchained import Resource, request, injectable
from flask_unchained.bundles.security import auth_required, current_user

from ..services import DataService, IndexManager, WatchlistManager


class WatchlistResource(Resource):
    data_service: DataService = injectable
    index_manager: IndexManager = injectable
    watchlist_manager: WatchlistManager = injectable

    class Meta:
        member_param = '<string:key>'

    @auth_required
    def create(self):
        watchlist = self.watchlist_manager.create(**request.json, user=current_user)
        return self.jsonify({'watchlist': watchlist.name})

    def list(self):
        watchlists = [dict(key=index.ticker,
                           label=index.name)
                      for index in self.index_manager.all()] + [
            dict(key='most-actives', label='Most Actives'),
            dict(key='trending', label='Trending'),
        ]
        return self.jsonify(watchlists)

    def get(self, key):
        if key == 'most-actives':
            return dict(key=key,
                        label='Most Actives',
                        components=self.watchlist_manager.get_most_actives())
        elif key == 'trending':
            return dict(key=key,
                        label='Trending',
                        components=self.watchlist_manager.get_trending())

        index = self.index_manager.get_by(ticker=key)
        if index is not None:
            return self.jsonify(dict(
                key=index.ticker,
                label=index.name,
                components=[self.data_service.get_quote(equity.ticker)
                            for equity in index.equities],
            ))
