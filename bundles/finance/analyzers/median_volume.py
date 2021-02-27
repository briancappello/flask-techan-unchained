import numpy as np

from .base_symbol_analyzer import SymbolAnalyzer


class MedianVolume(SymbolAnalyzer):
    timeframes = ['1D']
    lookback = 200

    @classmethod
    def run(cls, df):
        return dict(median_volume=int(np.median(df.Volume)))
