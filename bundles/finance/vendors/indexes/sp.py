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

from bundles.finance.utils.wiki import get_wiki_table_df


SP500_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def get_sp_500_df():
    """A DataFrame of S&P 500 components

    Indexed by ticker with columns: company_name, sector, industry, date_added, headquarters
    """
    df = get_wiki_table_df(SP500_URL).drop(['sec_filings', 'cik'], axis=1)
    return df.rename(columns={'symbol': 'ticker',
                              'gics_sector': 'sector',
                              'gics_sub_industry': 'industry',
                              'date_first_added': 'date_added',
                              'headquarters_location': 'headquarters',
                              'security': 'company_name'}).set_index('ticker')
