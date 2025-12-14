from sqlalchemy.dialects.postgresql import JSONB

from fin_models.enums import Freq

from flask_unchained.bundles.sqlalchemy import db


class Stats(db.Model):
    class Meta:
        repr = ("id", "symbol", "day")
        unique_together = ("symbol", "day", "freq")
        created_at = None
        updated_at = None

    id = db.Column(db.BigInteger, primary_key=True)
    symbol = db.Column(db.String, index=True, nullable=False)
    day = db.Column(db.Date, index=True, nullable=False)
    freq = db.Column(db.Enum(Freq), index=True, nullable=False)
    stats = db.Column(JSONB)
