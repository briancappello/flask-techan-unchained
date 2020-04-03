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

from bundles.finance.utils.soup import get_soup
from bundles.finance.utils.wiki import get_wiki_table_df, wiki_components_list_to_df


DJI_URL = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
DJT_URL = 'https://en.wikipedia.org/wiki/Dow_Jones_Transportation_Average'
DJU_URL = 'https://en.wikipedia.org/wiki/Dow_Jones_Utility_Average'


def get_dji_df():
    """A DataFrame of DJI components

    Indexed by ticker with columns: company_name, exchange, industry, date_added, notes
    """
    df = get_wiki_table_df(DJI_URL).rename(columns={'company': 'company_name',
                                                    'symbol': 'ticker'})
    df.ticker = [x.split(':')[-1].strip() for x in df.ticker]
    return df.set_index('ticker')


def get_djt_df():
    """A DataFrame of DJT components

    Indexed by ticker with columns: company_name, industry
    """
    df = get_wiki_table_df(DJT_URL, 'ticker')
    return df.rename(columns={'corporation': 'company_name'})


def get_dju_df():
    """A DataFrame of DJU components

    Indexed by ticker with columns: company_name
    """
    soup = get_soup(DJU_URL)
    components_header = soup.find('span', attrs={'id': 'Components'}).parent
    components_list = components_header.find_next_sibling('ul')
    return wiki_components_list_to_df(components_list)
