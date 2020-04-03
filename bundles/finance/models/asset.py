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

from ..enums import AssetType
from .asset_data_vendor import AssetDataVendor


class Asset(db.Model):
    """
    Base class for tradable assets. Should not be used directly.
    """
    class Meta:
        repr = ('id', 'type', 'ticker')

    type = db.Column(db.Enum(AssetType))  # polymorphic discriminator column
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': AssetType.Asset,
    }

    # canonical ticker
    ticker = db.Column(db.String(16), index=True, unique=True)

    asset_data_vendors = db.relationship('AssetDataVendor', back_populates='asset',
                                         cascade='all, delete-orphan')
    data_vendors = db.association_proxy(
        'asset_data_vendors', 'data_vendor',
        creator=lambda data_vendor: AssetDataVendor(data_vendor=data_vendor))

    asset_watchlists = db.relationship('WatchlistAsset', back_populates='asset')

    market_id = db.foreign_key('Market')
    market = db.relationship('Market', back_populates='assets')

    country = db.association_proxy('market', 'country')
    currency = db.association_proxy('market', 'currency')
    exchange = db.association_proxy('market', 'exchange')
