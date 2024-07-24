import pandas as pd
import numpy as np
from app.strategies.base_strategy import BaseStrategy

class RelativeStrengthIndexStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, rsi_window=14, overbought=70, oversold=30):
        super().__init__(symbol, timeframe)
        self.rsi_window = rsi_window
        self.overbought = overbought
        self.oversold = oversold

    def calculate_rsi(self, data, window):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self, data):
        df = data.copy()
        df['rsi'] = self.calculate_rsi(df, self.rsi_window)
        
        df['signal'] = np.where(df['rsi'] < self.oversold, 1, 0)
        df['signal'] = np.where(df['rsi'] > self.overbought, -1, df['signal'])
        df['signal'] = df['signal'].diff()
        
        return df

    def get_parameters(self):
        return {
            'rsi_window': self.rsi_window,
            'overbought': self.overbought,
            'oversold': self.oversold
        }

    def set_parameters(self, parameters):
        self.rsi_window = parameters.get('rsi_window', self.rsi_window)
        self.overbought = parameters.get('overbought', self.overbought)
        self.oversold = parameters.get('oversold', self.oversold)