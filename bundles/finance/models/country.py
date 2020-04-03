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
from sqlalchemy import or_
from sqlalchemy.ext.hybrid import Comparator


class CountryCodeComparator(Comparator):
    def operate(self, op, other):
        return or_(op(self.expression.iso_code, other),
                   op(self.expression.iso_code3, other))


class CountryNameComparator(Comparator):
    def operate(self, op, other):
        return or_(op(self.expression._name, other),
                   op(self.expression.iso_name, other),
                   op(self.expression.native_name, other))


class Country(db.Model):
    class Meta:
        repr = ('id', 'code', 'name')

    iso_code = db.Column(db.String(2), index=True, unique=True)    # ISO 3166-1 alpha-2
    iso_code3 = db.Column(db.String(3), index=True, unique=True)   # ISO 3166-1 alpha-3
    iso_name = db.Column(db.String(64), index=True, unique=True)   # official english short name (ISO 3166/MA)
    _name = db.Column('name', db.String(64), index=True, nullable=True, unique=True)   # common english name
    _native_name = db.Column('native_name', db.String(64), nullable=True, unique=True)

    currency_id = db.foreign_key('Currency')
    currency = db.relationship('Currency', back_populates='countries')

    markets = db.relationship('Market', back_populates='country')

    @db.hybrid_property
    def code(self):
        return self.iso_code

    @code.comparator
    def code(cls):
        return CountryCodeComparator(cls)

    @db.hybrid_property
    def name(self):
        return self._name or self.iso_name

    @name.setter
    def name(self, name):
        self._name = name

    @name.comparator
    def name(cls):
        return CountryNameComparator(cls)

    @db.hybrid_property
    def native_name(self):
        return self._native_name or self.name

    @native_name.setter
    def native_name(self, native_name):
        self._native_name = native_name
