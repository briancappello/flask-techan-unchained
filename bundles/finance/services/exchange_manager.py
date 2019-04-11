from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Exchange


class ExchangeManager(ModelManager):
    class Meta:
        model = Exchange

    def create(self, abbrev, name, commit=False, **kwargs):
        return super().create(abbrev=abbrev, name=name, commit=commit, **kwargs)
