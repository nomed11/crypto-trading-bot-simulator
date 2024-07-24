import pandas as pd
import numpy as np
from app.strategies.base_strategy import BaseStrategy

class SimpleMovingAverageStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, short_window=10, long_window=30):
        super().__init__(symbol, timeframe)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        df = data.copy()
        df['short_ma'] = df['close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['close'].rolling(window=self.long_window).mean()
        
        df['signal'] = np.where(df['short_ma'] > df['long_ma'], 1, 0)
        df['signal'] = np.where(df['short_ma'] < df['long_ma'], -1, df['signal'])
        df['signal'] = df['signal'].diff()
        
        return df

    def get_parameters(self):
        return {
            'short_window': self.short_window,
            'long_window': self.long_window
        }

    def set_parameters(self, parameters):
        self.short_window = parameters.get('short_window', self.short_window)
        self.long_window = parameters.get('long_window', self.long_window)