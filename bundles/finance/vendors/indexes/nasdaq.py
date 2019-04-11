import pandas as pd
import requests


NDX_URL = 'https://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx'


def get_nasdaq_100_df():
    """
    A DataFrame of NASDAQ-100 components

    Indexed by ticker with columns: company_name
    """
    html = requests.get(NDX_URL).text
    start = 'var table_body = '
    start_idx = html.find(start)+len(start)
    table = html[start_idx:html.find(';var col', start_idx)]
    rows = eval(table)
    components = [{'ticker': row[0], 'company_name': row[1]} for row in rows]
    return pd.DataFrame.from_records(components, index='ticker')
