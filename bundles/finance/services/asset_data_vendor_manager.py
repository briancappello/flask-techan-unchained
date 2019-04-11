from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import AssetDataVendor


class AssetDataVendorManager(ModelManager):
    class Meta:
        model = AssetDataVendor

    def create(self, asset, data_vendor, commit=False, **kwargs):
        return super().create(asset=asset, data_vendor=data_vendor,
                              commit=commit, **kwargs)
