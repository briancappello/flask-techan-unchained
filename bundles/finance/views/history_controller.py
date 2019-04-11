import pandas as pd
import talib as ta

from flask_unchained import Controller, injectable, route, param_converter

from ..enums import Frequency
from ..models import Asset
from ..services.data_service import DataService
from ..services.index_manager import IndexManager
from ..services.marketstore_service import MarketstoreService


class HistoryController(Controller):
    data_service: DataService = injectable
    index_manager: IndexManager = injectable
    marketstore_service: MarketstoreService = injectable

    @route('/history/<string(upper=True):ticker>')
    @param_converter(ticker=Asset, frequency=Frequency)
    def history(self, asset: Asset, frequency: Frequency):
        df = self.marketstore_service.get_history(asset.ticker, frequency)
        return add_ta(df).rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
        }).to_json(orient='split'), 200


# FIXME move to DataService
def add_ta(df: pd.DataFrame) -> pd.DataFrame:
    df['sma100'] = ta.SMA(df['Close'], timeperiod=100)
    df['sma200'] = ta.SMA(df['Close'], timeperiod=200)
    df['bbands_upper'], df['sma20'], df['bbands_lower'] = ta.BBANDS(df['Close'],
                                                                    timeperiod=20)
    df['macd'], df['macd_signal'], df['macd_difference'] = ta.MACD(df['Close'])
    df['rsi'] = ta.RSI(df['Close'])  # 14
    df['stoch_k'], df['stoch_d'] = ta.STOCH(
        df['High'],
        df['Low'],
        df['Close'],
        fastk_period=14,
        slowk_period=3,
        slowd_period=3
    )
    return df
