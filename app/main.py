from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
from app.models.trading_bot import TradingBot
from app.strategies.simple_moving_average import SimpleMovingAverageStrategy
from app.strategies.relative_strength_index import RelativeStrengthIndexStrategy
from app.utils.backtest import run_backtest, generate_performance_report

app = FastAPI()

class BacktestRequest(BaseModel):
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    strategies: List[Dict[str, Any]]

@app.post("/backtest")
async def backtest(request: BacktestRequest):
    bots = []
    for strategy_config in request.strategies:
        if strategy_config['name'] == 'SMA':
            strategy = SimpleMovingAverageStrategy(request.symbol, request.timeframe, 
                                                   short_window=strategy_config.get('short_window', 10),
                                                   long_window=strategy_config.get('long_window', 30))
        elif strategy_config['name'] == 'RSI':
            strategy = RelativeStrengthIndexStrategy(request.symbol, request.timeframe,
                                                     rsi_window=strategy_config.get('rsi_window', 14),
                                                     overbought=strategy_config.get('overbought', 70),
                                                     oversold=strategy_config.get('oversold', 30))
        else:
            raise HTTPException(status_code=400, detail=f"Unknown strategy: {strategy_config['name']}")
        
        bot = TradingBot(request.symbol, request.timeframe, strategy)
        bots.append(bot)

    results = run_backtest(bots, request.start_date, request.end_date)
    performance_report = generate_performance_report(results)

    return {
        "results": results,
        "performance_report": performance_report.to_dict(orient='records')
    }

@app.get("/available-strategies")
async def get_available_strategies():
    return {
        "strategies": [
            {
                "name": "SMA",
                "parameters": ["short_window", "long_window"]
            },
            {
                "name": "RSI",
                "parameters": ["rsi_window", "overbought", "oversold"]
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)