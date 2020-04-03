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

import re
import pandas as pd

from .soup import get_soup, table_to_df

TICKER_IN_PARENTHESIS_RE = re.compile(r'(?P<company_name>.+) \((?P<ticker>[A-Z]+)\)')


def get_wiki_table_df(url, index_col=None, columns=None):
    """Returns the first table of a Wikipedia page as a DataFrame"""
    soup = get_soup(url)
    table = soup.find('table', attrs={'class': 'wikitable'})
    return table_to_df(table, index_col, columns)


def wiki_components_list_to_df(list_tag):
    d = {'ticker': [], 'company_name': []}
    for li in list_tag.find_all('li'):
        match = TICKER_IN_PARENTHESIS_RE.search(li.text)
        d['ticker'].append(match.group('ticker'))
        d['company_name'].append(match.group('company_name'))

    return pd.DataFrame(d).set_index('ticker')
