from fin_models.enums import Freq
from fin_models.services import store
from fin_models.vendors.yahoo import get_df

from bundles.finance.enums import Frequency

from flask_unchained import Service


class MarketstoreService(Service):
    def __init__(self):
        pass

    def get_symbols(self):
        return store.symbols()

    def write(self, df, tbk, *args, **kwargs):
        symbol, timeframe, attrgroup = tbk.split('/')
        raise NotImplementedError(f'attempting to write df for {symbol} with tf={timeframe}')
        self.store.write(symbol, df)

    def get_history(self, symbol, timeframe: Frequency, attrgroup="OHLCV",
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
            Frequency.Minutely: Freq.min_1,
            Frequency.FiveMinutely: Freq.min_5,
            Frequency.TenMinutely: Freq.min_10,
            Frequency.FifteenMinutely: Freq.min_15,
            Frequency.ThirtyMinutely: Freq.min_30,
            Frequency.Hourly: Freq.hour,
            Frequency.Daily: Freq.day,
            Frequency.Weekly: Freq.week,
            Frequency.Monthly: Freq.month,
            Frequency.Yearly: Freq.year,
        }
        df = store.get(symbol, fin_models_freqs[timeframe])
        if limit:
            return df[-limit:]
        return df

    def get_bulk_history(self, symbols, timeframe, attrgroup="OHLCV",
                         start=None, end=None, limit=None, limit_from_start=False):
        if isinstance(symbols, str):
            symbols = [symbols]
        return {symbol: self.get_history(symbol, timeframe, limit=limit)
                for symbol in symbols}
