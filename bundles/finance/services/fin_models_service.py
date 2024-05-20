from fin_models.store import Store
from fin_models.vendors.yahoo import get_df

from flask_unchained import Service


class MarketstoreService(Service):
    def __init__(self):
        self.store = Store()

    def get_symbols(self):
        return self.store.symbols()

    def write(self, df, tbk, *args, **kwargs):
        symbol, timeframe, attrgroup = tbk.split('/')
        self.store.write(symbol, df)

    def get_history(self, symbol, timeframe, attrgroup="OHLCV",
                    start=None, end=None, limit=None, limit_from_start=False):
        if not self.store.has(symbol):
            df = get_df(symbol)
            self.store.write(symbol, df)
        df = self.store.get(symbol)
        if limit:
            return df[-limit:]
        return df

    def get_bulk_history(self, symbols, timeframe, attrgroup="OHLCV",
                         start=None, end=None, limit=None, limit_from_start=False):
        if isinstance(symbols, str):
            symbols = [symbols]
        return {symbol: self.get_history(symbol, timeframe, limit=limit)
                for symbol in symbols}
