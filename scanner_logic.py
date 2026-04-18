import pandas as pd
from engine import MomentumEngine
from mock_data import get_mock_l2
import random

MOCK_MODE = True # SET TO FALSE ON MONDAY

engine = MomentumEngine(alpha=0.2)

def run_funnel(watchlist):
    results = []
    
    for ticker in watchlist:
        # Stage 1: Get Order Book (Mock or Live)
        if MOCK_MODE:
            l2_data = get_mock_l2(ticker)
        else:
            # This is where your TradierClient call will go on Monday
            l2_data = {'bids': [], 'asks': []} 

        # Stage 2: Calculate Momentum
        score = engine.calculate_score(ticker, l2_data)
        
        # Stage 3: Mock Option Data (Lotto Filters)
        # We simulate the 0.01 - 0.05 spreads you want to find
        mock_spread = random.choice([0.01, 0.02, 0.05, 0.10])
        mock_price = random.uniform(0.05, 0.95)

        results.append({
            'Ticker': ticker,
            'Score': score,
            'Option_Price': round(mock_price, 2),
            'Spread': mock_spread,
            'Volume_M': round(random.uniform(1, 50), 1)
        })
        
    return pd.DataFrame(results)
