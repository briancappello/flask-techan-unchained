import functools
import numpy as np
import pandas as pd
import requests

from cachetools import cached, TTLCache
from datetime import date, datetime, time, timedelta, timezone
from dateutil.parser import parse as _parse_dt
from dateutil.tz import gettz
from urllib.parse import urlencode

from bundles.finance.utils import get_soup, table_to_df
from bundles.finance.utils.pandas import kmbt_to_int, to_float, to_percent

BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}'

EST = gettz('America/New_York')
BST = gettz('Europe/London')
CEST = gettz('Europe/Berlin')
IST = gettz('Asia/Kolkata')

# alias dateutil.parser.parse here to more sensible name/defaults
parse_datetime = functools.partial(
    _parse_dt,
    default=datetime.combine(datetime.now(), time(0, tzinfo=timezone.utc)),
    tzinfos={'EDT': EST, 'BST': BST, 'CEST': CEST, 'IST': IST},
)


def to_datetime(dt):
    if isinstance(dt, int):
        return datetime.fromtimestamp(dt)
    elif isinstance(dt, pd.Timestamp):
        return dt.to_pydatetime()
    elif isinstance(dt, datetime):
        return dt
    elif isinstance(dt, date):
        return datetime(*dt.timetuple()[:6])
    return parse_datetime(dt)


def to_est(dt: datetime):
    return dt.astimezone(EST)


def sanitize_dates(start=None, end=None, timeframe='1d'):
    if end is None:
        end = date.today() + timedelta(days=1)
    end = to_datetime(end)

    if start is None:
        days = 7 if timeframe == '1m' else (365*100 - 1)  # 100 years(ish)
        start = end - timedelta(days=days)
    start = to_datetime(start)

    return to_est(start), to_est(end)


def get_yfi_url(ticker, start=None, end=None, timeframe='1d'):
    start, end = sanitize_dates(start, end, timeframe)
    q = {'symbol': ticker,
         'period1': int(start.timestamp()),
         'period2': int(end.timestamp()),
         'interval': timeframe,
         'includePrePost': 'false',
         'events': 'div|split|earn',
         'corsDomain': 'finance.yahoo.com',
         }
    return BASE_URL.format(ticker=ticker, query=urlencode(q))


def yfi_json_to_df(json, timeframe='1d'):
    result = json['chart']
    if result['error']:
        print(result['error'])
        return None

    data = result['result'][0]
    try:
        quotes = data['indicators']['quote'][0]
        index = pd.DatetimeIndex(
            pd.to_datetime(data['timestamp'], unit='s'), name='Epoch'
        ).tz_localize('America/New_York')
        if timeframe == '1d':
            index = index.normalize()
        df = pd.DataFrame(quotes, index=index)
        df.volume = df.volume.fillna(0).astype('int64')
        df = df.fillna(method='ffill').sort_index()
        df.rename(columns=lambda name: name.title(), inplace=True)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        if not len(df) or timeframe != '1d':
            return df

        # check if 2 or more rows for the latest date
        tail = df[df.iloc[-1].name.date():]
        if len(tail) == 1:
            return df

        # and if so, pick the best daily bar by greatest volume
        latest = tail.sort_values('Volume').iloc[-1]
        return df[:df.iloc[-1].name.date()].append(latest)
    except Exception as e:
        print(str(e), '\n', data)
        return None


def get_df(ticker, start=None, end=None, timeframe='1d'):
    url = get_yfi_url(ticker, start, end, timeframe)
    r = requests.get(url)

    if r.status_code != 200:
        print(url, r.status_code, r.headers, r.content)
        return None

    return yfi_json_to_df(r.json(), timeframe)


@cached(cache=TTLCache(maxsize=1, ttl=60*60*4))  # 4 hours
def get_yfi_crumb_and_cookies():
    r = requests.get('https://finance.yahoo.com/most-active', headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    })
    html = str(r.content)
    start_search = '"CrumbStore":{"crumb":"'
    start_idx = html.find(start_search) + len(start_search)
    crumb = html[start_idx:html.find('"}', start_idx)]
    return crumb, r.cookies


def get_most_actives(
        region: str = 'us',
        min_intraday_vol: int = 250_000,
        min_intraday_price: float = 1.0,
        num_results: int = 100,
) -> pd.DataFrame:
    crumb, cookies = get_yfi_crumb_and_cookies()

    url = 'https://query1.finance.yahoo.com/v1/finance/screener?' + urlencode({
        'lang': 'en-US',
        'region': region.upper(),
        'formatted': 'true',
        'corsDomain': 'finance.yahoo.com',
        'crumb': crumb,
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
        'Host': 'query1.finance.yahoo.com',
        'Origin': 'https://finance.yahoo.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }, cookies=cookies)

    data = r.json()['finance']
    if 'error' in data and data['error']:
        raise Exception(str(data['error']))

    df = pd.DataFrame.from_records([
        {k: v['raw'] if isinstance(v, dict) else v for k, v in quote.items()}
        for quote in data['result'][0]['quotes']
    ], index='symbol')

    # drop junk data before returning (some kind of yahoo-specific (testing?) symbol)
    return df.drop('YTESTQFTACHYON')


def get_trending_tickers():
    url = 'https://finance.yahoo.com/trending-tickers'
    soup = get_soup(url)
    table = soup.find(attrs={'id': 'list-res-table'}).find('table')
    df = table_to_df(table, index_col='symbol')

    df = (df.drop(['day_chart', 'week_range', 'intraday_high_low'], axis=1)
            .rename(columns={'%_change': 'pct_change'})
            .replace('-', np.nan)
            .replace('N/A', np.nan)
            .dropna())

    df['last_price'] = df['last_price'].apply(to_float)
    df['change'] = df['change'].apply(to_float)
    df['pct_change'] = df['pct_change'].apply(to_percent)
    df['volume'] = df['volume'].apply(kmbt_to_int)
    df['market_cap'] = df['market_cap'].apply(kmbt_to_int)

    # FIXME: yahoo only returns the current time on business days, what does it
    # return on the weekends? do we need to set the correct date to the last
    # trading day, or does yahoo also return the date string when queried on
    # the weekends?
    df['market_time'] = pd.to_datetime(
        [parse_datetime(dt) for dt in df['market_time']], utc=True)
    return df
