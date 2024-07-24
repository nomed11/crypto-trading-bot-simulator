import pytest
import pandas as pd
from app.strategies.simple_moving_average import SimpleMovingAverageStrategy
from app.strategies.relative_strength_index import RelativeStrengthIndexStrategy

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'open': [100, 101, 102, 103, 104],
        'high': [102, 103, 104, 105, 106],
        'low': [99, 100, 101, 102, 103],
        'close': [101, 102, 103, 104, 105],
        'volume': [1000, 1100, 1200, 1300, 1400]
    }, index=pd.date_range(start='2023-01-01', periods=5))

def test_sma_strategy(sample_data):
    strategy = SimpleMovingAverageStrategy('BTC/USDT', '1h', short_window=2, long_window=3)
    result = strategy.generate_signals(sample_data)
    
    assert 'signal' in result.columns
    assert 'short_ma' in result.columns
    assert 'long_ma' in result.columns
    assert not result['signal'].isna().all()

def test_rsi_strategy(sample_data):
    strategy = RelativeStrengthIndexStrategy('BTC/USDT', '1h', rsi_window=2)
    result = strategy.generate_signals(sample_data)
    
    assert 'signal' in result.columns
    assert 'rsi' in result.columns
    assert not result['signal'].isna().all()

def test_strategy_parameter_management():
    sma_strategy = SimpleMovingAverageStrategy('BTC/USDT', '1h')
    rsi_strategy = RelativeStrengthIndexStrategy('BTC/USDT', '1h')

    sma_params = sma_strategy.get_parameters()
    assert 'short_window' in sma_params
    assert 'long_window' in sma_params

    rsi_params = rsi_strategy.get_parameters()
    assert 'rsi_window' in rsi_params
    assert 'overbought' in rsi_params
    assert 'oversold' in rsi_params

    new_sma_params = {'short_window': 5, 'long_window': 15}
    sma_strategy.set_parameters(new_sma_params)
    updated_sma_params = sma_strategy.get_parameters()
    assert updated_sma_params['short_window'] == 5
    assert updated_sma_params['long_window'] == 15

    new_rsi_params = {'rsi_window': 10, 'overbought': 75, 'oversold': 25}
    rsi_strategy.set_parameters(new_rsi_params)
    updated_rsi_params = rsi_strategy.get_parameters()
    assert updated_rsi_params['rsi_window'] == 10
    assert updated_rsi_params['overbought'] == 75
    assert updated_rsi_params['oversold'] == 25