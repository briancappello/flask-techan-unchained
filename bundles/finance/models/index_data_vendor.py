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


class IndexDataVendor(db.Model):
    """Join table between Index and DataVendor"""
    class Meta:
        repr = ('index_id', 'data_vendor_id', 'ticker')

    index_id = db.foreign_key('Index', primary_key=True)
    index = db.relationship('Index', back_populates='index_data_vendors')

    data_vendor_id = db.foreign_key('DataVendor', primary_key=True)
    data_vendor = db.relationship('DataVendor', back_populates='data_vendor_indexes')

    # vendor-specific index ticker (if different from canonical index ticker)
    _ticker = db.Column('ticker', db.String(16), nullable=True)

    def __init__(self, index=None, data_vendor=None, **kwargs):
        super(IndexDataVendor, self).__init__(**kwargs)
        if index:
            self.index = index
        if data_vendor:
            self.data_vendor = data_vendor

    @db.hybrid_property
    def ticker(self):
        return self._ticker or self.index.ticker

    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker
