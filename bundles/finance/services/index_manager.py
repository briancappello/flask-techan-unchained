from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Index


class IndexManager(ModelManager):
    class Meta:
        model = Index

    def create(self, ticker, name, commit=False, **kwargs):
        return super().create(ticker=ticker, name=name, commit=commit, **kwargs)

    def find_by_tickers(self, tickers):
        return self.filter(self.Meta.model.ticker.in_(tickers))
