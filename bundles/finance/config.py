import os

from flask_unchained import BundleConfig


class Config(BundleConfig):
    JSON_WATCHLISTS_PATH = os.path.join(os.path.expanduser('~'), 'watchlists.json')
