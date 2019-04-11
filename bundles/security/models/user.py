from flask_unchained.bundles.security.models import User as BaseUser
from flask_unchained.bundles.sqlalchemy import db


class User(BaseUser):
    class Meta:
        repr = ('id', 'username', 'email')

    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    watchlists = db.relationship('Watchlist', back_populates='user')
