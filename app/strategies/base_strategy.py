from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe

    @abstractmethod
    def generate_signals(self, data):
        """
        Generate buy/sell signals based on the strategy.
        
        :param data: DataFrame containing OHLCV data
        :return: DataFrame with additional 'signal' column (1 for buy, -1 for sell, 0 for hold)
        """
        pass

    @abstractmethod
    def get_parameters(self):
        """
        Return a dictionary of strategy parameters.
        """
        pass

    @abstractmethod
    def set_parameters(self, parameters):
        """
        Set strategy parameters.
        
        :param parameters: Dictionary of parameters to set
        """
        pass