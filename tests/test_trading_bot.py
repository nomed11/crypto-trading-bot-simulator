import pytest
from datetime import datetime, timedelta
from app.models.trading_bot import TradingBot
from app.strategies.simple_moving_average import SimpleMovingAverageStrategy
from app.strategies.relative_strength_index import RelativeStrengthIndexStrategy

@pytest.fixture
def sma_bot():
    strategy = SimpleMovingAverageStrategy('BTC/USD', '1h')
    return TradingBot('BTC/USD', '1h', strategy)

@pytest.fixture
def rsi_bot():
    strategy = RelativeStrengthIndexStrategy('BTC/USD', '1h')
    return TradingBot('BTC/USD', '1h', strategy)

def test_sma_bot_initialization(sma_bot):
    assert sma_bot.symbol == 'BTC/USD'
    assert sma_bot.timeframe == '1h'
    assert isinstance(sma_bot.strategy, SimpleMovingAverageStrategy)

def test_rsi_bot_initialization(rsi_bot):
    assert rsi_bot.symbol == 'BTC/USD'
    assert rsi_bot.timeframe == '1h'
    assert isinstance(rsi_bot.strategy, RelativeStrengthIndexStrategy)

def test_sma_bot_simulation(sma_bot):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    result = sma_bot.run_simulation(start_date, end_date)
    
    assert 'initial_balance' in result
    assert 'final_value' in result
    assert 'return' in result
    assert 'trades' in result
    assert isinstance(result['trades'], list)

def test_rsi_bot_simulation(rsi_bot):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    result = rsi_bot.run_simulation(start_date, end_date)
    
    assert 'initial_balance' in result
    assert 'final_value' in result
    assert 'return' in result
    assert 'trades' in result
    assert isinstance(result['trades'], list)

def test_strategy_parameter_management(sma_bot):
    initial_params = sma_bot.get_strategy_parameters()
    assert 'short_window' in initial_params
    assert 'long_window' in initial_params

    new_params = {'short_window': 5, 'long_window': 15}
    sma_bot.set_strategy_parameters(new_params)
    updated_params = sma_bot.get_strategy_parameters()
    
    assert updated_params['short_window'] == 5
    assert updated_params['long_window'] == 15