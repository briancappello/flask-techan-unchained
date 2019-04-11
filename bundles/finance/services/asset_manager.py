from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Asset


class AssetManager(ModelManager):
    class Meta:
        model = Asset

    def create(self, commit=False, **kwargs):
        return super().create(commit=commit, **kwargs)

    def find_by_types(self, asset_types):
        return self.q.filter(self.model.type.in_(asset_types)).all()
