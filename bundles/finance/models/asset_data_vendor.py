from flask_unchained.bundles.sqlalchemy import db


class AssetDataVendor(db.Model):
    """Join table between Asset and DataVendor"""
    class Meta:
        repr = ('asset_id', 'data_vendor_id', 'ticker')

    asset_id = db.foreign_key('Asset', primary_key=True)
    asset = db.relationship('Asset', back_populates='asset_data_vendors')

    data_vendor_id = db.foreign_key('DataVendor', primary_key=True)
    data_vendor = db.relationship('DataVendor', back_populates='data_vendor_assets')

    # vendor-specific ticker (if different from canonical ticker)
    _ticker = db.Column('ticker', db.String(16), nullable=True)

    minutely_last_updated = db.Column(db.DateTime(), nullable=True)
    daily_last_updated = db.Column(db.DateTime(), nullable=True)
    weekly_last_updated = db.Column(db.DateTime(), nullable=True)
    monthly_last_updated = db.Column(db.DateTime(), nullable=True)

    def __init__(self, asset=None, data_vendor=None, **kwargs):
        super(AssetDataVendor, self).__init__(**kwargs)
        if asset:
            self.asset = asset
        if data_vendor:
            self.data_vendor = data_vendor

    @db.hybrid_property
    def ticker(self):
        return self._ticker or self.asset.ticker

    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker
