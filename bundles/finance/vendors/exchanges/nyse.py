from .nasdaq import nasdaq_csv_to_df


NYSE_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'


def get_nyse_df():
    """A DataFrame of NYSE listed equities

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return nasdaq_csv_to_df(NYSE_URL)
