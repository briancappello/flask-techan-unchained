# Flask Techan Unchained
#
# Copyright (C) 2020  Brian Cappello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
                      for index in self.index_manager.all()
                      if 'Russell' not in index.name] + [
            dict(key='most-actives', label='Most Actives'),
            dict(key='trending', label='Trending'),
        ]
        return self.jsonify(watchlists)

    def get(self, key):
        if key == 'most-actives':
            return dict(key=key, components=self.watchlist_manager.get_most_actives())
        elif key == 'trending':
            return dict(key=key, components=self.watchlist_manager.get_trending())

        # fall back to returning index components
        index = self.index_manager.get_by(ticker=key)
        if index is not None:
            return self.jsonify(dict(
                key=index.ticker,
                components=[self.data_service.get_quote(equity.ticker)
                            for equity in index.equities],
            ))
