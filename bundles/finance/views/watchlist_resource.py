from flask_unchained import Resource, request, injectable
from flask_unchained.bundles.security import auth_required, current_user
from flask_unchained.string_utils import title_case

from ..services import DataService, HistoricalSignalsService, IndexManager, WatchlistManager


class WatchlistResource(Resource):
    data_service: DataService = injectable
    historical_signals_service: HistoricalSignalsService = injectable
    index_manager: IndexManager = injectable
    watchlist_manager: WatchlistManager = injectable

    class Meta:
        member_param = '<string:key>'

    @auth_required
    def create(self):
        watchlist = self.watchlist_manager.create(**request.json, user=current_user)
        return self.jsonify({'watchlist': watchlist.name})

    def list(self):
        watchlists = [
            dict(key=index.ticker, label=index.name)
            for index in self.index_manager.all()
            if 'Russell' not in index.name
         ] + [
            dict(key='most-actives', label='Most Actives'),
            dict(key='trending', label='Trending'),
            dict(key='gainers', label='Gainers'),
            dict(key='losers', label='Losers'),
        ] + [
            dict(key=signal.name, label=signal.label)
            for signal in self.historical_signals_service.signals
        ]
        return self.jsonify(watchlists)

    def get(self, key):
        try:
            return self.watchlist_manager.get_watchlist(key)
        except RuntimeError:
            pass

        # fall back to returning index components
        index = self.index_manager.get_by(ticker=key)
        if index is not None:
            return dict(
                key=index.ticker,
                components=self.data_service.get_quotes(
                    [equity.ticker for equity in index.equities]
                ),
            )
