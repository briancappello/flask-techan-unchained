import pandas as pd
import pystore
import trading_calendars as tc

from datetime import date

"""
analyze in:
    start_date
    symbols
    root_dir
    analyzers_module_name

interface to fetch data given symbol, timeframe, end_date, limit
interface to store results given timeframe + dataframe

filter in:
    start_date
    timeframe_dfs ?

interface to fetch data given timeframe + date
interface to store results given date +
"""

class Analyze:
    analyzers_module_name = 'bundles.finance.analyzers'
    filters_module_name = 'bundles.finance.filters'

    def __init__(self, start_date=None, end_date=None):
        self.nyse: tc.TradingCalendar = tc.get_calendar('NYSE')
        self.store = pystore.store('finance')

        today = pd.Timestamp(date.today(), tz='UTC')
        end_date = end_date and pd.Timestamp(end_date, tz='UTC') or (
            today if self.nyse.is_session(today) else self.nyse.previous_close(today)
        )
        start_date = start_date and pd.Timestamp(start_date, tz='UTC') or end_date
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        for day in self.sessions:
            next_session = self.nyse.next_session_label(day)
            filter_results = self.fetch_collection(f'filters-{day.isoformat()}')
            buys, sells = self.get_trades(filter_results)
            # enter trades at *next* open price

    @property
    def sessions(self):
        return self.nyse.sessions_in_range(self.start_date, self.end_date)

    def fetch(self, collection, name):
        return self.collection(collection).item(name).to_pandas(parse_dates=False)

    def fetch_collection(self, name):
        data = {}
        collection = self.collection(name)
        for item in collection.list_items():
            data[item] = collection.item(item).to_pandas(parse_dates=False)
        return data

    def collection(self, name):
        return self.store.collection(name)
