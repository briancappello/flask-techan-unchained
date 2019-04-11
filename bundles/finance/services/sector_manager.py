from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Sector


class SectorManager(ModelManager):
    class Meta:
        model = Sector

    def create(self, name, commit=False, **kwargs):
        return super().create(name=name, commit=commit, **kwargs)
