from app.data.data_fetcher import DataFetcher
from app.strategies.base_strategy import BaseStrategy
from typing import Dict, Any
import pandas as pd

class TradingBot:
    data_fetcher = DataFetcher('coinbase')

    def __init__(self, symbol: str, timeframe: str, strategy: BaseStrategy, initial_balance: float = 10000):
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0

    def run_simulation(self, start_date, end_date) -> Dict[str, Any]:
        data = self.data_fetcher.fetch_historical_data(self.symbol, self.timeframe, start_date, end_date)
        signals = self.strategy.generate_signals(data)
        
        self.balance = self.initial_balance
        self.position = 0
        trades = []

        for index, row in signals.iterrows():
            if row['signal'] == 1:  # buy signal
                if self.position == 0:
                    self.position = self.balance / row['close']
                    self.balance = 0
                    trades.append({
                        'date': index,
                        'type': 'buy',
                        'price': row['close'],
                        'amount': self.position
                    })
            elif row['signal'] == -1:  # sell signal
                if self.position > 0:
                    self.balance = self.position * row['close']
                    self.position = 0
                    trades.append({
                        'date': index,
                        'type': 'sell',
                        'price': row['close'],
                        'amount': self.balance
                    })

        final_value = self.balance + (self.position * signals.iloc[-1]['close'])
        return {
            'initial_balance': self.initial_balance,
            'final_value': final_value,
            'return': (final_value - self.initial_balance) / self.initial_balance * 100,
            'trades': trades
        }

    def get_strategy_parameters(self) -> Dict[str, Any]:
        return self.strategy.get_parameters()

    def set_strategy_parameters(self, parameters: Dict[str, Any]):
        self.strategy.set_parameters(parameters)