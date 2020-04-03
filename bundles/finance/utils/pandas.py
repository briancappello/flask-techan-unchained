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

import html


def str_strip(s):
    try:
        return s.strip()
    except AttributeError:
        return s


def to_float(f):
    try:
        return float(f)
    except ValueError:
        return f


def to_int(i):
    try:
        return int(i)
    except ValueError:
        return i


def kmbt_to_int(s):
    multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}
    for suffix, multiplier in multipliers.items():
        if s.endswith(suffix):
            return int(float(s.replace(',', '').replace(suffix, '')) * multiplier)
    return int(s.replace(',', ''))


def to_percent(s):
    try:
        return float(s.rstrip('%'))
    except ValueError:
        return s


def html_unescape(s):
    try:
        return html.unescape(s)
    except TypeError:
        return s
