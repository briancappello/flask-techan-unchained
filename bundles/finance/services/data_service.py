import pandas as pd

from flask_unchained.bundles.sqlalchemy import SessionManager
from flask_unchained import BaseService, injectable
from typing import *

from ..vendors import exchanges, indexes

from .country_manager import CountryManager
from .currency_manager import CurrencyManager
from .equity_manager import EquityManager
from .exchange_manager import ExchangeManager
from .index_manager import IndexManager
from .industry_manager import IndustryManager
from .market_manager import MarketManager
from .marketstore_service import MarketstoreService
from .sector_manager import SectorManager


class DataService(BaseService):
    country_manager: CountryManager = injectable
    currency_manager: CurrencyManager = injectable
    equity_manager: EquityManager = injectable
    exchange_manager: ExchangeManager = injectable
    index_manager: IndexManager = injectable
    industry_manager: IndustryManager = injectable
    market_manager: MarketManager = injectable
    marketstore_service: MarketstoreService = injectable
    sector_manager: SectorManager = injectable
    session_manager: SessionManager = injectable

    def __init__(self, print_fn=None):
        self.print_fn = print_fn

    def print(self, *args, **kwargs):
        if self.print_fn:
            self.print_fn(*args, **kwargs)

    def init(self):
        usd, _ = self.currency_manager.get_or_create(
            iso_name='United States dollar',
            name='dollar',
            iso_code='USD',
            symbol='$',
        )

        usa, _ = self.country_manager.get_or_create(
            iso_name='United States of America',
            name='United States',
            iso_code='US',
            iso_code3='USA',
            defaults=dict(
                currency=usd,
            ),
        )

        # exchange markets
        # ================
        nyse, _ = self.exchange_manager.get_or_create(
            abbrev='NYSE',
            name='New York Stock Exchange',
        )
        nasdaq, _ = self.exchange_manager.get_or_create(
            abbrev='NASDAQ',
            name='National Association of Securities Dealers Automated Quotations',
        )

        self._add_market({
            'abbrev': 'AMEX',
            'name': 'NYSE American',
            'defaults': {
                'exchange': nyse,
                'country': usa,
            },
        }, exchanges.amex.get_amex_df())

        self._add_market({
            'abbrev': 'NYSE',
            'name': 'New York Stock Exchange',
            'defaults': {
                'exchange': nyse,
                'country': usa,
            },
        }, exchanges.nyse.get_nyse_df())

        self._add_market({
            'abbrev': 'NASDAQ_GS',
            'name': 'NASDAQ Global Select Market',
            'defaults': {
                'exchange': nasdaq,
                'country': usa,
            },
        }, exchanges.nasdaq.get_nasdaq_gs_df())

        self._add_market({
            'abbrev': 'NASDAQ_GM',
            'name': 'NASDAQ Global Market',
            'defaults': {
                'exchange': nasdaq,
                'country': usa,
            },
        }, exchanges.nasdaq.get_nasdaq_gm_df())

        self._add_market({
            'abbrev': 'NASDAQ_CM',
            'name': 'NASDAQ Common Market',
            'defaults': {
                'exchange': nasdaq,
                'country': usa,
            },
        }, exchanges.nasdaq.get_nasdaq_cm_df())

        # index tickers
        # =============
        self._add_index({
            'ticker': '^DJI',
            'name': 'Dow Jones Industrial Average',
        }, indexes.dowjones.get_dji_df().index)

        self._add_index({
            'ticker': '^DJT',
            'name': 'Dow Jones Transportation Average',
        }, indexes.dowjones.get_djt_df().index)

        self._add_index({
            'ticker': '^DJU',
            'name': 'Dow Jones Utility Average',
        }, indexes.dowjones.get_dju_df().index)

        self._add_index({
            'ticker': '^NDX',
            'name': 'NASDAQ-100',
        }, indexes.nasdaq.get_nasdaq_100_df().index)

        self._add_index({
            'ticker': '^R1000',
            'name': 'Russell 1000',
        }, indexes.russell.get_russell_1000_tickers())

        # self._add_index({
        #     'ticker': '^R2000',
        #     'name': 'Russell 2000',
        # }, indexes.russell.get_russell_2000_tickers())
        #
        # self._add_index({
        #     'ticker': '^R3000',
        #     'name': 'Russell 3000',
        # }, indexes.russell.get_russell_3000_tickers())

        self._add_index({
            'ticker': '^SP500',
            'name': 'S&P 500',
        }, indexes.sp.get_sp_500_df().index)

        # FIXME
        # data vendors
        # ============
        # yahoo = DataVendor.create(key='yahoo', name='Yahoo! Finance')
        # av = DataVendor.create(key='av', name='Alpha Vantage')

    def _add_market(self, market_kwargs, df):
        """Add an exchange market

        :param dict market_kwargs: attributes to initialize the Market model with
        :param pd.DataFrame df: DataFrame of tickers traded on the market
        """
        market, _ = self.market_manager.get_or_create(**market_kwargs)

        sectors = {}
        industries = {}

        for sector_name, group in df.groupby('sector'):
            sector, sector_created = self.sector_manager.get_or_create(name=sector_name)
            sectors[sector_name] = sector

            for industry_name in group.industry.unique():
                if industry_name in industries:
                    industry = industries[industry_name]
                else:
                    industry, _ = self.industry_manager.get_or_create(name=industry_name)
                    industries[industry_name] = industry

                with self.session_manager.no_autoflush:
                    if industry not in sector.industries:
                        sector.industries.append(industry)

        for company_name, share_classes in df.groupby('company_name'):
            share_classes = (share_classes
                             .sort_values('sector')
                             .fillna(method='pad')
                             .sort_values('market_cap', ascending=False))

            sector, industry = None, None
            sector_name = share_classes.iloc[0].sector
            industry_name = share_classes.iloc[0].industry
            if not pd.isnull(sector_name):
                sector = sectors[sector_name]
                industry = industries[industry_name]

            # add the first ticker and any others where market cap is non 0
            # (we can't only filter on market cap because missing data :/ )
            tickers = set(share_classes[share_classes.market_cap > 0].index)
            for ticker in tickers.union({share_classes.index[0]}):
                equity, _ = self.equity_manager.update_or_create(
                    ticker=ticker,
                    defaults=dict(
                        market=market,
                        company_name=company_name,
                        sector=sector,
                        industry=industry,
                    ))

        self.session_manager.commit()
        self.print('Added {} {} tickers'.format(len(market.assets), market.name))

    def _add_index(self, index_kwargs, tickers):
        index, _ = self.index_manager.get_or_create(**index_kwargs)

        for ticker in tickers:
            equity = self.equity_manager.get_by(ticker=ticker)
            if not equity:
                self.print('WARNING: Missing Equity for ticker {}'.format(ticker))
                continue
            with self.session_manager.no_autoflush:
                if equity not in index.equities:
                    index.equities.append(equity)

        self.session_manager.commit()
        self.print('Added {} {} tickers'.format(len(index.equities), index.name))

    def get_quotes(self, tickers: Iterable[str]):
        return [self.get_quote(t) for t in tickers]

    def get_quote(self, ticker: str):
        df = self.marketstore_service.get_history(ticker, '1D', limit=2)
        prev_bar = df.iloc[-2]
        bar = df.iloc[-1]
        return dict(ticker=ticker,
                    date=bar.name,
                    open=bar.Open,
                    high=bar.High,
                    low=bar.Low,
                    close=bar.Close,
                    volume=bar.Volume,
                    prev_close=prev_bar.Close)
