import pandas as pd
import talib
from numpy import histogram
from flask_unchained.string_utils import snake_case, title_case

from . import analysis


class SignalNameDescriptor:
    def __get__(self, instance, cls):
        return snake_case(cls.__name__)


class SignalLabelDescriptor:
    def __get__(self, instance, cls):
        return title_case(cls.__name__)


class Signal:
    name: str = SignalNameDescriptor()
    label: str = SignalLabelDescriptor()
    window: int = 1

    def run(self, symbol, df: pd.DataFrame) -> bool:
        """
        FIXME: this interface works for daily or longer timeframes
        """
        raise NotImplementedError


class ExpandingBodies(Signal):
    window = 250

    def run(self, symbol, df: pd.DataFrame) -> bool:
        if analysis.is_expanding_bodies(df) and analysis.is_expanding_volume(df):
            two_days_ago = analysis.num_bars_since_prev_high(df[:-2])
            yesterday = analysis.num_bars_since_prev_high(df[:-1])
            today = analysis.num_bars_since_prev_high(df)
            if today > 100 and yesterday < 10 and two_days_ago < 10:
                return True
        return False


class LowRSI(Signal):
    window = 15
    threshold = 25
    label = 'Low RSI'

    def run(self, symbol, df: pd.DataFrame) -> bool:
        rsi = talib.RSI(df.Close, timeperiod=14)
        return rsi[-1] < self.threshold


class CrossedSMA200(Signal):
    label = 'Crossed SMA200'
    window = 200
    within_bars = 2
    min_multiple_of_median_volume = 2

    def run(self, symbol, df: pd.DataFrame) -> bool:
        crossed_sma = analysis.crossed_ma(df, ma=self.window,
                                          within_bars=self.within_bars)
        volume_multiple = analysis.volume_multiple_of_median(df)
        if crossed_sma and volume_multiple > self.min_multiple_of_median_volume:
            return True
        return False


"""
signals to code

>100% aftermarket movers

VTNR 2021-05-26 16:31
ENOB 2021-06-14 07:30
ALF 2021-06-15 08:06
ORPH 2021-06-10 11:15ish (news? wtf)
AHPI 2021-07-13 9:30ish
NURO 2021-07-20 9:00ish
XBIO 2021-07-23 9:00ish
NAOV 2021-07-23 1:30ish
FLGC 2021-07-26 3:30ish
PROG 2021-09-29 5:35ish
PROG 2021-10-11 12:00ish

- breakout new high
    - in > 2000 bars
- expanding high volume
    - increasing slope of MA
    - min median volume multiple OR(?) min median volume level
        * median multiple > 20x
        * mean multiple > 10x

"""


class NewHighs(Signal):
    """
    FIXME breakout new highs (this also catches new highs in uptrends)
    - abnormally high volume
    - abnormally large body
    """
    window = 300
    min_multiple_of_median_volume = 2

    def run(self, symbol, df: pd.DataFrame) -> bool:
        if df.Close.iloc[-1] < df.Open.iloc[-1]:
            return False

        yesterday = analysis.num_bars_since_prev_high(df[:-1])
        today = analysis.num_bars_since_prev_high(df)
        volume_multiple = analysis.volume_multiple_of_median(df)
        if yesterday < 5 and today > 250 and volume_multiple > self.min_multiple_of_median_volume:
            return True
        return False


class HighVolume(Signal):
    window = 100

    def run(self, symbol, df: pd.DataFrame) -> bool:
        if analysis.volume_multiple_of_median(df) >= 2 and analysis.volume_sum_of_prior_days(df) > 4:
            return True
        return False
