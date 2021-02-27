from .base_symbol_analyzer import SymbolAnalyzer


class Prices(SymbolAnalyzer):
    @classmethod
    def run(cls, df):
        return dict(
            open=df.Open.iloc[-1],
            high=df.High.iloc[-1],
            low=df.Low.iloc[-1],
            close=df.Close.iloc[-1],
            volume=df.Volume.iloc[-1],
            prev_close=df.Close.iloc[-2] if len(df) > 2 else None,
        )
