from flask_unchained import BundleConfig


class Config(BundleConfig):
    SIGNALS_MODULE = 'bundles.finance.signals'
    DATA_DIR = '/home/antonio/.fin-models-data'
