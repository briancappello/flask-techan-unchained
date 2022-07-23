import importlib
import inspect
import json
import os
import pandas as pd
import re

from datetime import date
from typing import *

from flask_unchained import Service, injectable

from .. import analysis
from ..signals import Signal
from .marketstore_service import MarketstoreService


VALID_SYMBOL_RE = re.compile(r'[A-Z]+')


def get_subclasses_in_module(module, base_class):
    """
    returns: List[Tuple(name, subclass)]
    """
    module = isinstance(module, str) and importlib.import_module(module) or module
    return list(inspect.getmembers(
        module,
        lambda o: (isinstance(o, type)
                   and issubclass(o, base_class)
                   and o != base_class)
    ))


class HistoricalSignalsService(Service):
    config = injectable
    marketstore_service: MarketstoreService = injectable

    def __init__(self):
        self.module_name: str = self.config.SIGNALS_MODULE
        self.signals: List[Signal] = self.get_signals()
        self.signal_names = [signal.name for signal in self.signals]

    def get_by_date(self, date: Optional[date] = None):
        date = date or analysis.get_latest_trading_date()
        filepath = self.get_filepath(date)
        if not os.path.exists(filepath):
            self.run(end_date=date)

        with open(filepath) as f:
            return json.load(f)

    def get_data(self,
                 symbols: Optional[List[str]] = None,
                 timeframe: str = '1D',
                 limit: int = 200,
                 end_date: Optional[Union[str, date, pd.Timestamp]] = None,
                 is_trading_safe: Optional[Callable[[pd.DataFrame], bool]] = None,
                 ) -> Iterator[Tuple[str, pd.DataFrame]]:
        symbols = symbols or self.marketstore_service.get_symbols()
        is_trading_safe = is_trading_safe or (lambda df: True)
        data = self.marketstore_service.get_bulk_history(
            symbols, timeframe, limit=limit, end=end_date)
        for symbol, df in data.items():
            if is_trading_safe(df):
                yield symbol, df

    def get_signals(self, module_name: Optional[str] = None) -> List[Signal]:
        module_name = module_name or self.module_name
        return [t[1]() for t in get_subclasses_in_module(module_name, Signal)]

    def run(self,
            symbols: Optional[List[str]] = None,
            timeframe: str = '1D',
            end_date: Optional[Union[str, date, pd.Timestamp]] = None,
            is_trading_safe: Optional[Callable[[pd.DataFrame], bool]] = None,
            module_name: Optional[str] = None,
            ) -> Dict[str, Any]:
        """
        FIXME: parallelize
        """
        symbols = symbols or self.marketstore_service.get_symbols()
        signals = self.get_signals(module_name) if module_name else self.signals
        max_window = max(signal.window for signal in signals)

        if end_date is None:
            end_date = analysis.get_latest_trading_date()
        elif isinstance(end_date, str):
            end_date = pd.Timestamp(end_date).date()
        elif isinstance(end_date, pd.Timestamp):
            end_date = end_date.date()

        results = dict(date=end_date.isoformat(),
                       results={signal.name: [] for signal in signals})

        for symbol, df in self.get_data(
                symbols=[symbol for symbol in symbols
                         if VALID_SYMBOL_RE.match(symbol)],
                timeframe=timeframe,
                limit=max_window,
                end_date=end_date,
                is_trading_safe=is_trading_safe,
        ):
            ts = df.index[-1]
            if ts.date() != end_date or not VALID_SYMBOL_RE.match(symbol):
                continue
            for signal in signals:
                if signal.run(symbol, df):
                    results['results'][signal.name].append(symbol)
        self.persist_results(results)
        return results

    def get_filepath(self, date: date):
        return os.path.join(self.config.APP_DATA_FOLDER,
                            'signals', f'{date}.json')

    def persist_results(self, results: Dict[str, Any]):
        date = results['date']
        filepath = self.get_filepath(date)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(results['results'], f, indent=4)
