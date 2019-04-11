from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Market


class MarketManager(ModelManager):
    class Meta:
        model = Market

    def create(self, abbrev, name, exchange, country, commit=False, **kwargs):
        return super().create(abbrev=abbrev, name=name, exchange=exchange,
                              country=country, commit=commit, **kwargs)
