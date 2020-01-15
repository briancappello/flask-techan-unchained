import functools
import numpy as np
import pandas as pd
import requests

from cachetools import cached, TTLCache
from datetime import date, datetime, time, timedelta, timezone
from dateutil.parser import parse as _parse_dt
from dateutil.tz import gettz
from urllib.parse import urlencode

from bundles.finance.utils import clean_df, get_soup, table_to_df
from bundles.finance.utils.pandas import kmbt_to_int, to_float, to_percent

BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}'

EST = gettz('America/New_York')
BST = gettz('Europe/London')

# alias dateutil.parser.parse here to more sensible name/defaults
parse_datetime = functools.partial(_parse_dt,
                                   default=datetime.combine(
                                       datetime.now(),
                                       time(0, tzinfo=timezone.utc)),
                                   tzinfos={'EDT': EST, 'BST': BST})


def to_datetime(dt):
    if not dt:
        return None
    elif isinstance(dt, pd.Timestamp):
        return dt.to_pydatetime()
    elif isinstance(dt, datetime):
        return dt
    elif isinstance(dt, date):
        return datetime(*dt.timetuple()[:6])
    return parse_datetime(dt)


def to_est(dt: datetime):
    return dt.astimezone(EST)


def sanitize_dates(start=None, end=None):
    end = to_datetime(end)
    if end is None:
        end = datetime.now()

    start = to_datetime(start)
    if start is None:
        start = end - timedelta(days=(365*100) - 1)  # 100 years(ish) minus 1 day

    return to_est(start), to_est(end)


def clean_df(df):
    df.volume = df.volume.fillna(0).astype('int64')
    return df.fillna(method='ffill')


def get_daily_url(ticker, start=None, end=None):
    start, end = sanitize_dates(start, end)
    q = {'symbol': ticker,
         'period1': int(start.timestamp()),
         'period2': int(end.timestamp()),
         'interval': '1d',
         'includePrePost': 'false',
         'events': 'div|split|earn',
         'corsDomain': 'finance.yahoo.com',
         }
    return BASE_URL.format(ticker=ticker, query=urlencode(q))


def daily_json_to_df(json):
    result = json['chart']
    if result['error']:
        print(result['error'])
        return None

    data = result['result'][0]
    try:
        quotes = data['indicators']['quote'][0]
        dates = pd.to_datetime(data['timestamp'], unit='s')
        # dates = pd.to_datetime(data['timestamp'], unit='s').date
        index = pd.DatetimeIndex(dates, name='datetime')
        df = pd.DataFrame(quotes, index=index)
        df = clean_df(df).sort_index()
        df = df[['open', 'high', 'low', 'close', 'volume']]
        if not len(df):
            return df

        # check if 2 or more rows for the latest date
        tail = df[df.iloc[-1].name.date():]
        if len(tail) == 1:
            return df

        # and if so, pick the best daily bar by greatest volume
        latest = tail.sort_values('volume').iloc[-1]
        return df[:df.iloc[-1].name.date()].append(latest)
    except Exception as e:
        print(str(e), '\n', data)
        return None


def get_daily_df(ticker, start=None, end=None):
    url = get_daily_url(ticker, start, end)
    r = requests.get(url)

    if r.status_code != 200:
        print(url, r.status_code, r.headers, r.content)
        return None

    return daily_json_to_df(r.json())


@cached(cache=TTLCache(maxsize=1, ttl=60*60*24))  # 24 hours
def get_yfi_crumb():
    html = str(requests.get('https://finance.yahoo.com/most-active').content)
    start_idx = html.find('"CrumbStore"')
    crumb = html[start_idx:html.find('"}', start_idx)]
    return crumb[crumb.rfind('"')+1:]


def get_most_actives(
        region='us',
        min_intraday_vol=2.5e5,
        min_intraday_price=2,
        num_results=100
) -> pd.DataFrame:
    url = 'https://query2.finance.yahoo.com/v1/finance/screener?' + urlencode({
        'lang': 'en-US',
        'region': region.upper(),
        'formatted': 'true',
        'corsDomain': 'finance.yahoo.com',
        'crumb': get_yfi_crumb(),
    })

    r = requests.post(url, json={
        'offset': 0,
        'size': num_results,
        'sortField': 'dayvolume',
        'sortType': 'DESC',
        'quoteType': 'EQUITY',
        'query': {
            'operator': 'AND',
            'operands': [
                {'operator': 'eq', 'operands': ['region', region.lower()]},
                {'operator': 'gt', 'operands': ['dayvolume', int(min_intraday_vol)]},
                {'operator': 'gt', 'operands': ['intradayprice', float(min_intraday_price)]},
            ],
        },
        'userId': '',
        'userIdType': 'guid',
    }, headers={
        'Host': 'query2.finance.yahoo.com',
        'Origin': 'https://finance.yahoo.com',
    })

    quotes = r.json()['finance']['result'][0]['quotes']
    df = pd.DataFrame.from_records([
        {k: v['raw'] if isinstance(v, dict) else v for k, v in quote.items()}
        for quote in quotes
    ], index='symbol')

    # drop junk data before returning (some kind of yahoo-specific (testing?) symbol)
    return df.drop('YTESTQFTACHYON')


def get_trending_tickers():
    url = 'https://finance.yahoo.com/trending-tickers'
    soup = get_soup(url)
    table = soup.find('table', attrs={'class': 'yfinlist-table'})
    df = table_to_df(table, index_col='symbol')

    renames = {'change': ['change', 'pct_change'],
               'avg_vol____month': ['avg_volume']}
    df = (df.drop(['day_chart', 'week_range', 'intraday_high_low'], axis=1)
            .rename(columns=lambda c: renames[c].pop(0) if renames.get(c, []) else c)
            .replace('-', np.nan)
            .dropna())

    df['last_price'] = df['last_price'].apply(to_float)
    df['change'] = df['change'].apply(to_float)
    df['pct_change'] = df['pct_change'].apply(to_percent)
    df['volume'] = df['volume'].apply(kmbt_to_int)
    df['avg_volume'] = df['avg_volume'].apply(kmbt_to_int)
    df['market_cap'] = df['market_cap'].apply(kmbt_to_int)

    # FIXME: yahoo only returns the current time on business days, what does it
    # return on the weekends? do we need to set the correct date to the last
    # trading day, or does yahoo also return the date string when queried on
    # the weekends?
    df['market_time'] = pd.to_datetime(
        [parse_datetime(dt) for dt in df['market_time']], utc=True)
    return df
