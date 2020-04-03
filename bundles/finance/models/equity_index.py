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


class EquityIndex(db.Model):
    """Join table between Equity and Index"""
    class Meta:
        repr = ('equity', 'index')

    equity_id = db.foreign_key('Equity', primary_key=True)
    equity = db.relationship('Equity', back_populates='equity_indexes')

    index_id = db.foreign_key('Index', primary_key=True)
    index = db.relationship('Index', back_populates='index_equities')

    def __init__(self, equity=None, index=None, **kwargs):
        super().__init__(**kwargs)
        if equity:
            self.equity = equity
        if index:
            self.index = index
