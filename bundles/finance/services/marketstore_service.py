import os

import pandas as pd

from flask_unchained import Service

from ..enums import Frequency


class MarketstoreService(Service):
    def __init__(self, config):
        self.data_dir = config.DATA_DIR

    def get_symbols(self):
        _, _, filenames = next(os.walk(self.data_dir), (None, None, []))
        return [f.split('.')[0] for f in filenames]

    def write(self, df, tbk, isvariablelength=False):
        pass

    def get_history(self, symbol, timeframe, attrgroup='OHLCV',
                    start=None, end=None,
                    limit=None, limit_from_start=False):
        if not self.has(symbol, timeframe):
            return None
        return pd.read_pickle(self._path(symbol))

    def get_bulk_history(self, symbols, timeframe, attrgroup='OHLCV',
                         start=None, end=None,
                         limit=None, limit_from_start=False):
        if isinstance(symbols, str):
            symbols = [symbols]
        return {symbol: self.get_history(symbol, timeframe)
                for symbol in symbols}

    def has(self, symbol, timeframe):
        if timeframe not in {'D', '1D', Frequency.Daily}:
            raise RuntimeError(timeframe)
            return False
        return os.path.exists(self._path(symbol))

    def _path(self, symbol):
        return f'{self.data_dir.rstrip("/")}/{symbol}.pickle'
