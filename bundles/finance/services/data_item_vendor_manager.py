from flask_unchained.bundles.sqlalchemy import ModelManager

from ..models import DataItem, DataItemVendor, DataVendor


class DataItemVendorManager(ModelManager):
    class Meta:
        model = DataItemVendor

    def create(self,
               data_item: DataItem,
               data_vendor: DataVendor,
               priority: int,
               commit: bool = False,
               **kwargs,
               ) -> DataItemVendor:
        return super().create(data_item=data_item,
                              data_vendor=data_vendor,
                              priority=priority,
                              commit=commit,
                              **kwargs)
