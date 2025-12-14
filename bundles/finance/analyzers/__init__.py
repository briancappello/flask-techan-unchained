"""
analyzers
---------
per day:
    in: symbols
        parallelize
            in: symbol
            out: one row per symbol per timeframe
    out: dict(timeframe: { analyzer_columns: values })


opportunity filters
-------------------
per day:
    in: timeframe analysis dataframes
        in: each filter
        out: name of filter, list of symbols matched


results/
    date/
        list-assets.json (what's tradable, shortable, etc)
        1Min-analysis.df
        15Min-analysis.df
        30Min-analysis.df
        1D-analysis.df
        1W-analysis.df
        1M-analysis.df
        opportunities.json { <key=filter_name>: <value=[LIST, OF, SYMBOLS]> }
"""
import numpy as np
import talib as ta

from .base_symbol_analyzer import SymbolAnalyzer
from .runner import AnalyzersRunner


class Prices(SymbolAnalyzer):
    timeframes = ['1D']

    @classmethod
    def run(cls, df):
        return dict(
            open=df.Open.iloc[-1],
            high=df.High.iloc[-1],
            low=df.Low.iloc[-1],
            close=df.Close.iloc[-1],
            volume=df.Volume.iloc[-1],
            prev_close=df.Close.iloc[-2] if len(df) > 2 else None,
        )


class MedianVolume(SymbolAnalyzer):
    timeframes = ['1D']
    lookback = 200

    @classmethod
    def run(cls, df):
        try:
            return dict(median_volume=int(np.median(df.Volume)))
        except (ValueError, TypeError):
            return dict(median_volume=None)


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
