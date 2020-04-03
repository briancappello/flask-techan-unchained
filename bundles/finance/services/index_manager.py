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

from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Index


class IndexManager(ModelManager):
    class Meta:
        model = Index

    def create(self, ticker, name, commit=False, **kwargs):
        return super().create(ticker=ticker, name=name, commit=commit, **kwargs)

    def find_by_tickers(self, tickers):
        return self.filter(self.Meta.model.ticker.in_(tickers))
