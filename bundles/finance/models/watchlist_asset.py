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

from flask_unchained.bundles.sqlalchemy import db


class WatchlistAsset(db.Model):
    asset_id = db.foreign_key('Asset', primary_key=True)
    asset = db.relationship('Asset', back_populates='asset_watchlists')

    watchlist_id = db.foreign_key('Watchlist', primary_key=True)
    watchlist = db.relationship('Watchlist', back_populates='watchlist_assets')

    def __init__(self, asset=None, watchlist=None, **kwargs):
        super().__init__(**kwargs)
        if asset is not None:
            self.asset = asset
        if watchlist is not None:
            self.watchlist = watchlist
