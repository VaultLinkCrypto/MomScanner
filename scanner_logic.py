import pandas as pd
from mock_data import get_mock_l2
import random

def run_funnel(watchlist, engine):
    results = []
    for ticker in watchlist:
        # Fetch data
        l2_data = get_mock_l2(ticker)
        
        # Update the numbers
        score = engine.calculate_score(ticker, l2_data)
        is_active = ticker in engine.active_tickers
        
        # We simulate these for the weekend
        mock_price = round(random.uniform(0.10, 0.95), 2)
        mock_spread = random.choice([0.01, 0.02, 0.05, 0.10, 0.15])

        results.append({
            'Ticker': ticker,
            'Score': score,
            'Status': '🔥 ACTIVE' if is_active else '🔎 SCANNING',
            'Option_Price': mock_price,
            'Spread': mock_spread
        })
    return pd.DataFrame(results)
