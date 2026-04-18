import pandas as pd
from mock_data import get_mock_l2
import random

def run_funnel(watchlist, engine):
    results = []
    for ticker in watchlist:
        # 1. Fetch the mock data (This generates new random sizes every call)
        l2_data = get_mock_l2(ticker)
        
        # 2. Update the numbers in the Engine
        score = engine.calculate_score(ticker, l2_data)
        is_active = ticker in engine.active_tickers
        
        # 3. Create dynamic mock values for the weekend
        # These will change every second to prove the dashboard is LIVE
        mock_price = round(random.uniform(0.10, 0.95), 2)
        mock_spread = random.choice([0.01, 0.02, 0.05, 0.10])
        # This is the line that was missing:
        mock_volume = round(random.uniform(5.0, 50.0), 1) 

        results.append({
            'Ticker': ticker,
            'Score': score,
            'Status': '🔥 ACTIVE' if is_active else '🔎 SCANNING',
            'Option_Price': mock_price,
            'Spread': mock_spread,
            'Volume_M': mock_volume  # Re-added the volume column
        })
    return pd.DataFrame(results)
