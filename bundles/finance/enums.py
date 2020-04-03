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

from enum import Enum, EnumMeta


class ByNameAndValueEnumMeta(EnumMeta):
    def __getitem__(self, name):
        try:
            return self._member_map_[name]
        except KeyError:
            return self._value2member_map_[name]


class AssetType(Enum):
    Asset = 'Asset'
    Equity = 'Equity'


class Frequency(Enum, metaclass=ByNameAndValueEnumMeta):
    Minutely = '1m'
    FiveMinutely = '5m'
    TenMinutely = '10m'
    FifteenMinutely = '15m'
    ThirtyMinutely = '30m'
    Hourly = '1hr'
    Daily = 'D'
    Weekly = 'W'
    Monthly = 'M'
    Yearly = 'Y'
