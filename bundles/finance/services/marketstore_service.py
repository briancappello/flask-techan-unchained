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

import numpy as np
import pymarketstore as pymkts
import re

from flask_unchained import Service

from ..enums import Frequency


TIMEFRAME_RE = re.compile('^([0-9]+)(Sec|Min|H|D|W|M|Y)')
TIMEFRAMES = {
    '1m': '1Min',
    '5m': '5Min',
    '10m': '10Min',
    '15m': '15Min',
    '30m': '30Min',
    '1hr': '1H',
    'D': '1D',
    'W': '1W',
    'M': '1M',
    'Y': '1Y',
}


def get_timeframe(timeframe):
    if isinstance(timeframe, Frequency):
        return TIMEFRAMES[timeframe.value]
    elif isinstance(timeframe, str) and timeframe in TIMEFRAMES:
        return TIMEFRAMES[timeframe]
    elif not isinstance(timeframe, str) or not TIMEFRAME_RE.match(timeframe):
        raise ValueError('Timeframe must be a string in the format of '
                         '[0-9]+(Sec|Min|H|D|W|M|Y)')
    return timeframe


class MarketstoreService(Service):
    def __init__(self, config):
        host = config.MARKETSTORE_RPC_HOST
        port = config.MARKETSTORE_RPC_PORT
        path = config.MARKETSTORE_RPC_PATH
        self.client = pymkts.Client(endpoint=f'http://{host}:{port}{path}')

    def get_symbols(self):
        return self.client.list_symbols()

    def write(self, df, tbk, isvariablelength=False):
        # rename lower case columns to title case
        df = df.rename(columns={name: name.title() for name in
                                ['open', 'high', 'low', 'close', 'volume']})

        # FIXME: convert float64 to float32 to make marketstore happy
        new_types = df.dtypes.map({
            np.dtype(np.float64): np.float32,
            np.dtype(np.int64): np.int32,
        }).to_dict()
        df = df.astype(new_types)

        return self.client.write(df, tbk, isvariablelength)

    def get_history(self, symbol, timeframe, attrgroup='OHLCV',
                    start=None, end=None,
                    limit=None, limit_from_start=False):
        p = pymkts.Param(symbol, get_timeframe(timeframe), attrgroup,
                         start=start, end=end,
                         limit=limit, limit_from_start=limit_from_start)
        try:
            return self.client.query(p).first().df()
        except Exception as e:
            if 'No files returned from query parse' in e.args[0]:
                return None
            raise e

    def get_bulk_history(self, symbols, timeframe, attrgroup='OHLCV',
                         start=None, end=None,
                         limit=None, limit_from_start=False):
        if isinstance(symbols, str):
            symbols = [symbols]

        p = pymkts.Param(','.join(symbols), get_timeframe(timeframe), attrgroup,
                         start=start, end=end,
                         limit=limit, limit_from_start=limit_from_start)
        r = self.client.query(p)
        return {symbol: ds.df() for symbol, ds in r.by_symbols()}
