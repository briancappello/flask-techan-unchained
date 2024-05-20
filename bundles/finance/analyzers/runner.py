import importlib
import inspect
import pandas as pd
# import pymarketstore as pymkts

from collections import defaultdict
from typing import *

from .base_symbol_analyzer import SymbolAnalyzer


class AnalyzersRunner:
    def __init__(self, analyzers_module_name, day=None):
        self.analyzers_module_name = analyzers_module_name
        self.day = day
        self.client = pymkts.Client()

    def run(self, symbol) -> Dict[str, Dict[str, Union[bool, int, float, str]]]:
        """
        returns a dict of dicts
        outer dict is keyed by timeframe, inner dict is keyed by column names
        """
        analyzers = self.get_analyzers()

        results: Dict[str, Dict[str, Union[bool, int, float, str]]] = {}
        for timeframe, analyzers in analyzers.items():
            df = self.get_data(symbol, timeframe, limits=[
                x.lookback for x in analyzers
            ])
            if not len(df):
                continue

            results[timeframe] = dict(symbol=symbol)
            for analyzer in analyzers:
                columns = set(results[timeframe].keys())
                data = analyzer.run(df)
                conflicts = columns & set(data.keys())
                if conflicts:
                    raise Exception('conflicting column name(s) between analyzers: '
                                    ', '.join(conflicts))

                results[timeframe].update(data)
        return results

    def get_data(self, symbol, timeframe, limits) -> pd.DataFrame:
        limit = None
        if all(isinstance(x, int) for x in limits):
            limit = max(*limits) if len(limits) > 1 else limits[0]
        return self.client.query(
            pymkts.Params(symbol, timeframe, attrgroup='OHLCV', limit=limit,
                          end=pd.Timestamp(self.day.date(), tz='America/New_York'))
        ).first().df()

    def get_analyzers(self) -> Dict[str, List[SymbolAnalyzer]]:
        module = importlib.import_module(self.analyzers_module_name)
        classes = inspect.getmembers(module, lambda x: (isinstance(x, type)
                                                        and issubclass(x, SymbolAnalyzer)
                                                        and x != SymbolAnalyzer))
        analyzers = defaultdict(list)
        for _, analyzer in classes:
            for timeframe in analyzer.timeframes:
                analyzers[timeframe].append(analyzer)
        return analyzers
