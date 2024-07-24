import pytest
from datetime import datetime, timedelta
from app.models.trading_bot import TradingBot
from app.strategies.simple_moving_average import SimpleMovingAverageStrategy
from app.strategies.relative_strength_index import RelativeStrengthIndexStrategy
from app.utils.backtest import run_backtest, generate_performance_report
from app.data.data_fetcher import DataFetcher

@pytest.fixture(scope="module")
def data_fetcher():
    return DataFetcher('coinbase')

@pytest.fixture(scope="module")
def sample_bots(data_fetcher):
    TradingBot.data_fetcher = data_fetcher
    sma_strategy = SimpleMovingAverageStrategy('BTC/USD', '1h')
    rsi_strategy = RelativeStrengthIndexStrategy('BTC/USD', '1h')
    sma_bot = TradingBot('BTC/USD', '1h', sma_strategy)
    rsi_bot = TradingBot('BTC/USD', '1h', rsi_strategy)
    return [sma_bot, rsi_bot]

@pytest.fixture(scope="module")
def backtest_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    return start_date, end_date

def test_run_backtest(sample_bots, backtest_dates):
    start_date, end_date = backtest_dates
    results = run_backtest(sample_bots, start_date, end_date)
    assert len(results) == 2
    for bot_result in results.values():
        assert 'initial_balance' in bot_result
        assert 'final_value' in bot_result
        assert 'return' in bot_result
        assert 'trades' in bot_result

def test_generate_performance_report(sample_bots, backtest_dates):
    start_date, end_date = backtest_dates
    backtest_results = run_backtest(sample_bots, start_date, end_date)
    report = generate_performance_report(backtest_results)
    assert len(report) == 2
    assert 'Strategy' in report.columns
    assert 'Initial Balance' in report.columns
    assert 'Final Value' in report.columns
    assert 'Return (%)' in report.columns
    assert 'Number of Trades' in report.columns

def test_backtest_different_timeframes(data_fetcher, backtest_dates):
    TradingBot.data_fetcher = data_fetcher
    start_date, end_date = backtest_dates
    sma_strategy_1h = SimpleMovingAverageStrategy('BTC/USD', '1h')
    sma_strategy_4h = SimpleMovingAverageStrategy('BTC/USD', '4h')
    bot_1h = TradingBot('BTC/USD', '1h', sma_strategy_1h)
    bot_4h = TradingBot('BTC/USD', '4h', sma_strategy_4h)
    results = run_backtest([bot_1h, bot_4h], start_date, end_date)
    assert len(results) == 2
    assert 'BTC/USD_SimpleMovingAverageStrategy' in results

def test_backtest_multiple_symbols(data_fetcher, backtest_dates):
    TradingBot.data_fetcher = data_fetcher
    start_date, end_date = backtest_dates
    sma_strategy_btc = SimpleMovingAverageStrategy('BTC/USD', '1h')
    sma_strategy_eth = SimpleMovingAverageStrategy('ETH/USD', '1h')
    bot_btc = TradingBot('BTC/USD', '1h', sma_strategy_btc)
    bot_eth = TradingBot('ETH/USD', '1h', sma_strategy_eth)
    results = run_backtest([bot_btc, bot_eth], start_date, end_date)
    assert len(results) == 2
    assert 'BTC/USD_SimpleMovingAverageStrategy' in results
    assert 'ETH/USD_SimpleMovingAverageStrategy' in results