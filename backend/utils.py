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

import functools
import pandas as pd
import re

from datetime import date, datetime, time, timezone
from dateutil.parser import parse as _parse_dt
from dateutil.tz import gettz

est = gettz('America/New_York')
bst = gettz('Europe/London')

# alias dateutil.parser.parse here to more sensible name/defaults
parse_datetime = functools.partial(_parse_dt,
                                   default=datetime.combine(
                                       datetime.now(),
                                       time(0, tzinfo=timezone.utc)),
                                   tzinfos={'EDT': est, 'BST': bst})


def timestamp_to_datetime(seconds, tz=None):
    """
    Returns a datetime.datetime of `seconds` in UTC

    :param seconds: timestamp relative to the epoch
    :param tz: timezone of the timestamp
    """
    if tz is None:
        tz = timezone.utc
    dt = datetime.fromtimestamp(seconds, tz)
    return dt.astimezone(timezone.utc)


def utcnow():
    return datetime.now(timezone.utc)


def to_datetime(dt):
    if not dt:
        return None
    elif isinstance(dt, pd.Timestamp):
        return dt.to_pydatetime()
    elif isinstance(dt, datetime):
        return dt
    elif isinstance(dt, date):
        return datetime(*dt.timetuple()[:6])
    return parse_datetime(dt)


def to_est(dt: datetime):
    return dt.astimezone(est)


def to_utc(dt: datetime):
    return dt.astimezone(timezone.utc)


def sanitize_dates(start=None, end=None):
    start = to_datetime(start)
    if start is None:
        start = datetime(1900, 1, 1)

    end = to_datetime(end)
    if end is None:
        end = datetime.now()

    return to_est(start), to_est(end)


# from django.utils.text
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
