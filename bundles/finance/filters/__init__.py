import pandas as pd

from typing import *

from .base_opportunity_filter import OpportunityFilter
from .runner import FiltersRunner


class HighVolume(OpportunityFilter):
    # min median volume of avg 100 shares traded per minute per day
    min_median_volume = 6.5 * 60 * 80
    min_multiple_of_median = 10

    @classmethod
    def run(cls,
            data: Dict[str, pd.DataFrame]
            ) -> pd.DataFrame:
        df = data['1D']
        results = []
        for symbol in df.index:
            row = df.loc[symbol]
            if (not row.volume or not row.median_volume
                    or row.median_volume < cls.min_median_volume):
                continue
            multiple_of_median = row.volume / row.median_volume
            if multiple_of_median > cls.min_multiple_of_median:
                results.append(dict(symbol=symbol,
                                    volume=row.volume,
                                    multiple_of_median_volume=multiple_of_median))
        return (pd.DataFrame.from_records(results, index='symbol')
                .sort_values('multiple_of_median_volume', ascending=False))


class LowRSI(OpportunityFilter):
    low_level = 30

    @classmethod
    def run(cls,
            data: Dict[str, pd.DataFrame],
            ) -> pd.DataFrame:
        df = data['1D']
        results = []
        for symbol in df.index:
            rsi = df.loc[symbol].rsi
            if rsi and rsi < cls.low_level:
                results.append(dict(symbol=symbol, rsi=rsi))
        return pd.DataFrame.from_records(results, index='symbol').sort_values('rsi')
