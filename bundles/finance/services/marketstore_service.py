import pymarketstore as pymkts
import re

from flask_unchained import BaseService

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


class MarketstoreService(BaseService):
    def __init__(self, config):
        host = config.MARKETSTORE_RPC_HOST
        port = config.MARKETSTORE_RPC_PORT
        path = config.MARKETSTORE_RPC_PATH
        self.client = pymkts.Client(endpoint=f'http://{host}:{port}{path}')

    def get_history(self, symbol, timeframe, attrgroup='OHLCV',
                    start=None, end=None,
                    limit=None, limit_from_start=False):
        p = pymkts.Param(symbol, get_timeframe(timeframe), attrgroup,
                         start=start, end=end,
                         limit=limit, limit_from_start=limit_from_start)
        return self.client.query(p).first().df()

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
