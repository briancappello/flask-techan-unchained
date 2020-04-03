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

from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import DataItem


class DataItemManager(ModelManager):
    class Meta:
        model = DataItem

    def create(self, key, update_frequency, update_at, commit=False, **kwargs):
        return super().create(key=key, update_frequency=update_frequency,
                              update_at=update_at, commit=commit, **kwargs)

    def get_by_key(self, key):
        return self.get_by(key=key)
