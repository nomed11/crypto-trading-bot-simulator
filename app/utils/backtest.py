import pandas as pd
from typing import List, Dict, Any
from app.models.trading_bot import TradingBot
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_backtest(bots: List[TradingBot], start_date, end_date) -> Dict[str, Any]:
    results = {}
    
    def run_single_backtest(bot):
        bot_result = bot.run_simulation(start_date, end_date)
        return f"{bot.symbol}_{bot.strategy.__class__.__name__}", bot_result

    with ThreadPoolExecutor() as executor:
        future_to_bot = {executor.submit(run_single_backtest, bot): bot for bot in bots}
        for future in as_completed(future_to_bot):
            key, result = future.result()
            results[key] = result

    return results

def generate_performance_report(backtest_results: Dict[str, Any]) -> pd.DataFrame:
    report_data = []
    for strategy_name, result in backtest_results.items():
        report_data.append({
            'Strategy': strategy_name,
            'Initial Balance': result['initial_balance'],
            'Final Value': result['final_value'],
            'Return (%)': result['return'],
            'Number of Trades': len(result['trades'])
        })
    return pd.DataFrame(report_data)

def plot_equity_curves(backtest_results: Dict[str, Any]):
    plt.figure(figsize=(12, 6))
    for strategy_name, result in backtest_results.items():
        equity_curve = [result['initial_balance']]
        for trade in result['trades']:
            if trade['type'] == 'sell':
                equity_curve.append(trade['amount'])
        
        plt.plot(equity_curve, label=strategy_name)

    plt.title('Equity Curves')
    plt.xlabel('Trades')
    plt.ylabel('Account Value')
    plt.legend()
    plt.grid(True)
    plt.show()