from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import DataVendor


class DataVendorManager(ModelManager):
    class Meta:
        model = DataVendor

    def create(self, key, name, commit=False, **kwargs):
        return super().create(key=key, name=name, commit=commit, **kwargs)
