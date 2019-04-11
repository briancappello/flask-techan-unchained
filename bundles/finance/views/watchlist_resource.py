from flask_unchained import Resource
from flask_unchained import injectable

from ..services.data_service import DataService
from ..services.index_manager import IndexManager


class WatchlistResource(Resource):
    data_service: DataService = injectable
    index_manager: IndexManager = injectable

    class Meta:
        member_param = '<string:key>'

    def list(self):
        watchlists = [dict(key=index.ticker,
                           label=index.name)
                      for index in self.index_manager.all()]
        return self.jsonify(watchlists)

    def get(self, key):
        index = self.index_manager.get_by(ticker=key)
        if index is not None:
            return self.jsonify(dict(
                key=index.ticker,
                label=index.name,
                components=[self.data_service.get_quote(equity.ticker)
                            for equity in index.equities],
            ))
