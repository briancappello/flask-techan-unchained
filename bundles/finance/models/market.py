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


class Market(db.Model):
    class Meta:
        repr = ('id', 'abbrev', 'name')

    abbrev = db.Column(db.String(16))
    name = db.Column(db.String(64))

    assets = db.relationship('Asset', back_populates='market')

    country_id = db.foreign_key('Country')
    country = db.relationship('Country', back_populates='markets')

    currency = db.association_proxy('country', 'currency')

    exchange_id = db.foreign_key('Exchange')
    exchange = db.relationship('Exchange', back_populates='markets')


# FIXME
'''
timezone

premarket open
market open
market close
aftermarket close

trading calendar from zipline?
'''
