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
from .asset import Asset
from .equity_index import EquityIndex


class Equity(Asset):
    class Meta:
        repr = ('id', 'ticker')

    __mapper_args__ = {
        'polymorphic_identity': AssetType.Equity,
    }

    id = db.foreign_key('Asset', primary_key=True)
    company_name = db.Column(db.String, index=True)
    company_description = db.Column(db.Text, nullable=True)

    equity_indexes = db.relationship('EquityIndex', back_populates='equity',
                                     cascade='all, delete-orphan')
    indexes = db.association_proxy('equity_indexes', 'index',
                                   creator=lambda equity: EquityIndex(equity=equity))

    sector_id = db.foreign_key('Sector', nullable=True)
    sector = db.relationship('Sector', back_populates='equities')

    industry_id = db.foreign_key('Industry', nullable=True)
    industry = db.relationship('Industry', back_populates='equities')

    # active = db.Column(Boolean(name='active'), default=True)  # active == listed & trading
