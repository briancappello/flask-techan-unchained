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

from .asset_data_vendor import AssetDataVendor
from .index_data_vendor import IndexDataVendor


class DataVendor(db.Model):
    class Meta:
        repr = ('id', 'key', 'name')

    key = db.Column(db.String(16), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    priority = db.Column(db.Integer)

    data_vendor_assets = db.relationship('AssetDataVendor', back_populates='data_vendor')
    assets = db.association_proxy(
        'data_vendor_assets', 'asset',
        creator=lambda asset: AssetDataVendor(asset=asset))

    data_vendor_indexes = db.relationship('IndexDataVendor', back_populates='data_vendor')
    indexes = db.association_proxy(
        'data_vendor_indexes', 'index',
        creator=lambda index: IndexDataVendor(index=index))

    data_vendor_items = db.relationship('DataItemVendor', back_populates='data_vendor')
    data_items = db.association_proxy('data_vendor_items', 'data_item')
