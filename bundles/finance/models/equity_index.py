from flask_unchained.bundles.sqlalchemy import db


class EquityIndex(db.Model):
    """Join table between Equity and Index"""
    class Meta:
        repr = ('equity_id', 'index_id')

    equity_id = db.foreign_key('Equity', primary_key=True)
    equity = db.relationship('Equity', back_populates='equity_indexes')

    index_id = db.foreign_key('Index', primary_key=True)
    index = db.relationship('Index', back_populates='index_equities')

    def __init__(self, equity=None, index=None, **kwargs):
        super(EquityIndex, self).__init__(**kwargs)
        if equity:
            self.equity = equity
        if index:
            self.index = index
