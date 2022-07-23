import pandas as pd
import pandas_market_calendars as mcal

from datetime import date, timedelta
from typing import *


NYSE = mcal.get_calendar('NYSE')


def get_latest_trading_date() -> date:
    today = date.today()
    return NYSE.valid_days(
        today - timedelta(days=5), today, tz='America/New_York',
    )[-1].date()


def is_market_open(timestamp: Optional[pd.Timestamp] = None) -> bool:
    ts = timestamp or pd.Timestamp.now(tz='America/New_York')
    schedule = NYSE.schedule(ts - pd.Timedelta(days=2), ts + pd.Timedelta(days=2))
    return NYSE.open_at_time(schedule, ts)
