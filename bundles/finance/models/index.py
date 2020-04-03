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

from .equity_index import EquityIndex


class Index(db.Model):
    class Meta:
        repr = ('id', 'ticker', 'name')

    ticker = db.Column(db.String(16), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)

    index_data_vendors = db.relationship('IndexDataVendor', back_populates='index')

    index_equities = db.relationship('EquityIndex', back_populates='index',
                                     cascade='all, delete-orphan')
    equities = db.association_proxy('index_equities', 'equity',
                                    creator=lambda equity: EquityIndex(equity=equity))
