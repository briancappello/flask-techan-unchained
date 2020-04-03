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
