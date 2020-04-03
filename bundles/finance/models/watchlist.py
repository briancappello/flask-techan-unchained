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

from .watchlist_asset import WatchlistAsset


class Watchlist(db.Model):
    class Meta:
        repr = ('id', 'name', 'user')

    name = db.Column(db.String, unique=True, index=True)

    user_id = db.foreign_key('User')
    user = db.relationship('User', back_populates='watchlists')

    watchlist_assets = db.relationship('WatchlistAsset', back_populates='watchlist',
                                       cascade='all, delete-orphan')
    assets = db.association_proxy('watchlist_assets', 'asset',
                                  creator=lambda asset: WatchlistAsset(asset=asset))
