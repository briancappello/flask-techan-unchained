import pandas as pd

from typing import *


class SymbolAnalyzer:
    timeframes = ['1D']
    attrgroup = 'OHLCV'
    lookback = 200

    @classmethod
    def run(cls, df: pd.DataFrame) -> Dict[str, Union[bool, int, float, str]]:
        raise NotImplementedError
