from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Country


class CountryManager(ModelManager):
    class Meta:
        model = Country

    def create(self, iso_name, name, iso_code, iso_code3, currency,
               commit=False, **kwargs):
        return super().create(iso_name=iso_name, name=name,
                              iso_code=iso_code, iso_code3=iso_code3,
                              currency=currency, commit=commit, **kwargs)
