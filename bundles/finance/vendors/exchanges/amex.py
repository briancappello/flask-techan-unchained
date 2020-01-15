from .nasdaq import nasdaq_csv_to_df


AMEX_URL = 'http://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'


def get_amex_df():
    """A DataFrame of AMEX listed equities

    Indexed by ticker with columns: company_name, last_sale, market_cap, sector, industry
    """
    return nasdaq_csv_to_df(AMEX_URL)
