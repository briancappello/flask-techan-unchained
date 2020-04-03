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


class DataItemVendor(db.Model):
    """
    join table between DataItem and DataVendor
    """
    class Meta:
        pk = None

    data_item_id = db.foreign_key('DataItem', primary_key=True)
    data_item = db.relationship('DataItem', back_populates='data_item_vendors')

    data_vendor_id = db.foreign_key('DataVendor', primary_key=True)
    data_vendor = db.relationship('DataVendor', back_populates='data_vendor_items')

    priority = db.Column(db.Integer, nullable=True)

    def __init__(self, data_item=None, data_vendor=None, priority=None, **kwargs):
        super().__init__(priority=priority, **kwargs)
        if data_item:
            self.data_item = data_item
        if data_vendor:
            self.data_vendor = data_vendor
