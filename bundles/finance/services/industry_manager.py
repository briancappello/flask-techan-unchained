from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import Industry


class IndustryManager(ModelManager):
    class Meta:
        model = Industry

    def create(self, name, commit=False, **kwargs):
        return super().create(name=name, commit=commit, **kwargs)
