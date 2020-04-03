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

from .soup import get_soup, table_to_df, find_after
from .wiki import get_wiki_table_df, wiki_components_list_to_df


class Abstractable(type):
    def __new__(mcs, name, bases, clsdict):
        if '__abstract__' not in clsdict:
            clsdict['__abstract__'] = False
        return super().__new__(mcs, name, bases, clsdict)


def clean_df(df):
    df.volume = df.volume.fillna(0).astype('int64')
    return df.fillna(method='ffill')
