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

from .data_item_vendor import DataItemVendor


class DataItem(db.Model):
    key = db.Column(db.String(32))
    update_frequency = db.Column(db.String(32))
    update_at = db.Column(db.String(32))

    data_item_vendors = db.relationship('DataItemVendor', back_populates='data_item')
    data_vendors = db.association_proxy(
        'data_item_vendors', 'data_vendor',
        creator=lambda item: DataItemVendor(data_item=item)
    )
