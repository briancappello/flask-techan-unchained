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

from .nasdaq import nasdaq_csv_to_df


AMEX_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'


def get_amex_df():
    """A DataFrame of AMEX listed equities

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return nasdaq_csv_to_df(AMEX_URL)
