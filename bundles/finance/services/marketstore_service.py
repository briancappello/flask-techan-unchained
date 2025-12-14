from fin_models.enums import Freq
from fin_models.services import store

from flask_unchained import Service


class MarketstoreService(Service):
    def __init__(self):
        pass

    def get_symbols(self):
        return store.symbols()

    def get_history(self, symbol, timeframe: Freq, attrgroup="OHLCV",
                    start=None, end=None, limit=None, limit_from_start=False):
        fin_models_freqs = {
            '1Min': Freq.min_1,
            '5Min': Freq.min_5,
            '10Min': Freq.min_10,
            '15Min': Freq.min_15,
            '30Min': Freq.min_30,
            '1H': Freq.hour,
            '1D': Freq.day,
            '1M': Freq.month,
            '1Y': Freq.year,
            None: Freq.min_1,
        }
        df = store.get(symbol, freq=fin_models_freqs.get(timeframe, timeframe))
        if df is not None and limit:
            return df[-limit:]
        return df

    def get_bulk_history(self, symbols, timeframe: Freq, attrgroup="OHLCV",
                         start=None, end=None, limit=None, limit_from_start=False):
        if isinstance(symbols, str):
            symbols = [symbols]
        return {symbol: self.get_history(symbol, timeframe, limit=limit)
                for symbol in symbols}
