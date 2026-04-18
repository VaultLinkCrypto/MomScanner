import pandas as pd
from mock_data import get_mock_l2
import random

def run_funnel(watchlist, engine):
    results = []
    for ticker in watchlist:
        # Get data (Mock for now, Tradier on Monday)
        l2_data = get_mock_l2(ticker)
        
        # Update the persistent engine
        score = engine.calculate_score(ticker, l2_data)
        
        # Check if it's currently in the VIP Lounge
        is_active = ticker in engine.active_tickers
        
        results.append({
            'Ticker': ticker,
            'Score': score,
            'Status': '🔥 ACTIVE' if is_active else '🔎 SCANNING',
            'Option_Price': round(random.uniform(0.10, 0.90), 2),
            'Spread': random.choice([0.01, 0.02, 0.05])
        })
    return pd.DataFrame(results)
