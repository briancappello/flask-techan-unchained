from flask_unchained.bundles.sqlalchemy import ModelManager


from ..models import Currency


class CurrencyManager(ModelManager):
    class Meta:
        model = Currency

    def create(self, iso_name, name, iso_code, symbol, commit=False, **kwargs):
        return super().create(iso_name=iso_name, name=name,
                              iso_code=iso_code, symbol=symbol,
                              commit=commit, **kwargs)
