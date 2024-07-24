import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
from functools import lru_cache

class DataFetcher:
    def __init__(self, exchange_name='coinbase'):
        self.exchange = getattr(ccxt, exchange_name)()
        self.data_cache = {}

    def fetch_historical_data(self, symbol, timeframe, start_date, end_date=None):
        cache_key = (symbol, timeframe, start_date, end_date)
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]

        if end_date is None:
            end_date = datetime.now()

        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)

        all_candles = []
        while start_timestamp < end_timestamp:
            try:
                candles = self.exchange.fetch_ohlcv(symbol, timeframe, start_timestamp)
                if not candles:
                    break
                all_candles.extend(candles)
                start_timestamp = candles[-1][0] + 1
            except ccxt.NetworkError as e:
                print(f"Network error: {str(e)}. Retrying in 5 seconds...")
                time.sleep(5)
            except ccxt.ExchangeError as e:
                print(f"Exchange error: {str(e)}. Retrying in 5 seconds...")
                time.sleep(5)

        df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        self.data_cache[cache_key] = df
        return df

    def get_latest_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.fetch_historical_data('BTC/USD', '1h', datetime.now() - timedelta(days=30))
    print(data.head())
    print(f"Latest BTC/USD price: {fetcher.get_latest_price('BTC/USD')}")