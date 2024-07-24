# Cryptocurrency Trading Bot Simulator

## Overview
This project implements a sophisticated cryptocurrency trading bot simulator that leverages historical data to backtest various trading strategies. It provides a robust framework for developing, testing, and analyzing algorithmic trading strategies in the cryptocurrency market.

## Features
- Fetch historical cryptocurrency data from Coinbase
- Implement and backtest multiple trading strategies
- Simulate trading with customizable initial balance and time frames
- Generate performance reports and equity curves
- API interface for running backtests and retrieving results

## Technologies Used
- Python 3.9+
- FastAPI for API development
- CCXT library for cryptocurrency exchange interactions
- Pandas for data manipulation and analysis
- NumPy for numerical computations
- Matplotlib for data visualization
- Pytest for unit and integration testing

## Project Structure
```
crypto-trading-bot-simulator/
├── app/
│   ├── data/
│   │   ├── data_fetcher.py
│   ├── models/
│   │   ├── trading_bot.py
│   ├── strategies/
│   │   ├── base_strategy.py
│   │   ├── simple_moving_average.py
│   │   ├── relative_strength_index.py
│   ├── utils/
│   │   ├── backtest.py
│   ├── main.py
├── tests/
│   ├── test_backtest.py
│   ├── test_trading_bot.py
│   ├── test_strategies.py
├── .gitignore
├── requirements.txt
├── README.md
```

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/nomed11/crypto-trading-bot-simulator.git
   cd crypto-trading-bot-simulator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Use the `/backtest` endpoint to run backtests with different strategies and parameters

## Example Usage

You can interact with the CryptoTrade Simulator through its API using curl or tools like Postman.

### Using curl

1. Run a backtest:

```bash
curl -X POST "http://localhost:8000/backtest" \
     -H "Content-Type: application/json" \
     -d '{
  "symbol": "BTC/USD",
  "timeframe": "1h",
  "start_date": "2023-06-01T00:00:00",
  "end_date": "2023-07-01T00:00:00",
  "strategies": [
    {
      "name": "SMA",
      "short_window": 10,
      "long_window": 30
    },
    {
      "name": "RSI",
      "rsi_window": 14,
      "overbought": 70,
      "oversold": 30
    }
  ]
}'
```

2. Get available strategies:

```bash
curl "http://localhost:8000/available-strategies"
```

### Using Postman

1. For the backtest endpoint:
   - Create a new POST request to `http://localhost:8000/backtest`
   - Add header: `Content-Type: application/json`
   - In the request body (raw JSON), use:

```json
{
  "symbol": "BTC/USD",
  "timeframe": "1h",
  "start_date": "2023-06-01T00:00:00",
  "end_date": "2023-07-01T00:00:00",
  "strategies": [
    {
      "name": "SMA",
      "short_window": 10,
      "long_window": 30
    },
    {
      "name": "RSI",
      "rsi_window": 14,
      "overbought": 70,
      "oversold": 30
    }
  ]
}
```

2. For available strategies:
   - Create a new GET request to `http://localhost:8000/available-strategies`

### Tips for Using the Simulator

- Modify the `symbol` to test different cryptocurrencies (e.g., "ETH/USD" for Ethereum)
- Adjust the `timeframe` for different intervals (e.g., "15m", "4h", "1d")
- Change `start_date` and `end_date` to backtest over different periods
- Experiment with strategy parameters to optimize performance
- Add multiple strategies to compare their performance under the same market conditions

For more detailed information about the endpoints and request/response formats, refer to the API documentation at `http://localhost:8000/docs`.

## Running Tests
Execute the test suite using pytest:
```
pytest
```

## Implemented Strategies
1. Simple Moving Average (SMA)
2. Relative Strength Index (RSI)

## Future Enhancements
- Implement additional trading strategies
- Add support for more cryptocurrency exchanges
- Develop a user interface for easier interaction and visualization
- Incorporate machine learning models for predictive analysis

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
