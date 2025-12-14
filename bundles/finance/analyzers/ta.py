import talib as ta

from .base_symbol_analyzer import SymbolAnalyzer


class TA(SymbolAnalyzer):
    timeframes = ['1D']
    lookback = 200

    @classmethod
    def run(cls, df):
        bbands_upper, sma20, bbands_lower = ta.BBANDS(df.Close[-20:], timeperiod=20)
        return dict(
            bbands_upper=bbands_upper[-1],
            sma20=sma20[-1],
            bbands_lower=bbands_lower[-1],
            rsi=ta.RSI(df.Close[-15:])[-1],
            sma100=ta.SMA(df.Close[-100:], timeperiod=100)[-1],
            sma200=ta.SMA(df.Close[-200:], timeperiod=200)[-1],
        )
