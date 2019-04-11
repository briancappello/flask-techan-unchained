from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Equity


class EquityManager(ModelManager):
    class Meta:
        model = Equity

    def create(self, ticker, company_name, market, commit=False, **kwargs):
        return super().create(ticker=ticker, company_name=company_name,
                              market=market, commit=commit, **kwargs)
