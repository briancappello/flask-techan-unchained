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

import pandas as pd
import re
import requests

from bs4 import BeautifulSoup, Tag


def get_soup(url):
    """Returns an instance of BeautifulSoup for the given URL"""
    return BeautifulSoup(requests.get(url).content, 'lxml')


def table_to_df(table, index_col=None, columns=None) -> pd.DataFrame:
    """Converts an HTML table to a DataFrame

    Uses the first row as the column labels, converted to snakecase
    """
    header, *rows = table.find_all('tr')
    cols = columns or [
        re.sub(r'[^a-z]', ' ', th.text.strip().lower()).strip().replace(' ', '_')
        for th in header.find_all('th')
    ]
    rows = [list(td.text.strip() for td in tr.find_all('td'))[:len(cols)]
            for tr in rows]
    df = pd.DataFrame(rows, columns=cols)
    if index_col:
        df.set_index(index_col, inplace=True)
    return df


def find_after(node, *find_args, **find_kwargs):
    """Like find, but searches siblings of the given node"""
    while True:
        if not node.next_sibling:
            return None
        node = node.next_sibling
        if not isinstance(node, Tag):
            continue
        result = node.find(*find_args, **find_kwargs)
        if result:
            return result
