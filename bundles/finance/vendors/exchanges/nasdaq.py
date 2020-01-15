import io
import pandas as pd
import requests

from bundles.finance.utils.pandas import html_unescape, str_strip


NASDAQ_GS_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&market=NGS&render=download'
NASDAQ_GM_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&market=NGM&render=download'
NASDAQ_CM_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&market=NCM&render=download'


def nasdaq_csv_to_df(url):
    """Converts a csv of NASDAQ equities to a DataFrame

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    cols = ['ticker', 'company_name', 'last_sale', 'market_cap', 'adr_tso',
            'ipo_year', 'sector', 'industry', 'url', '__empty__']
    use_cols = ['ticker', 'company_name', 'last_sale', 'market_cap',
                'sector', 'industry']
    return pd.read_csv(io.BytesIO(requests.get(url).content),
                       header=0,
                       names=cols,
                       usecols=use_cols,
                       index_col='ticker',
                       na_values=['n/a'],
                       converters={'ticker': str_strip,
                                   'company_name': html_unescape})


def _get_nasdaq_df(url):
    # even though we're pulling both NYSE and NASDAQ tickers from the same
    # source, the NASDAQ exchange lists still include a few erroneous tickers
    # that are actually traded on the NYSE (as verified manually on 9/22/17).
    # therefore we need to drop those duplicates
    from .nyse import get_nyse_df
    df = nasdaq_csv_to_df(url)
    nyse_df = get_nyse_df()
    return df.drop(nyse_df.index, errors='ignore')


def get_nasdaq_gs_df():
    """A DataFrame of NASDAQ Global Select Market listed equities (large cap)

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return _get_nasdaq_df(NASDAQ_GS_URL)


def get_nasdaq_gm_df():
    """A DataFrame of NASDAQ Global Market listed equities (mid cap)

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return _get_nasdaq_df(NASDAQ_GM_URL)


def get_nasdaq_cm_df():
    """A DataFrame of NASDAQ Common Market listed equities (small cap)

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return _get_nasdaq_df(NASDAQ_CM_URL)
