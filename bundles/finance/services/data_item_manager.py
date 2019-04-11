from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import DataItem


class DataItemManager(ModelManager):
    class Meta:
        model = DataItem

    def create(self, key, update_frequency, update_at, commit=False, **kwargs):
        return super().create(key=key, update_frequency=update_frequency,
                              update_at=update_at, commit=commit, **kwargs)

    def get_by_key(self, key):
        return self.get_by(key=key)
