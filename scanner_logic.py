import pandas as pd
from mock_data import get_mock_l2
import random
import time

def run_funnel(watchlist, engine):
    results = []
    for ticker in watchlist:
        # 1. Fetch data
        l2_data = get_mock_l2(ticker)
        
        # 2. Update numbers
        score = engine.calculate_score(ticker, l2_data)
        is_active = ticker in engine.active_tickers
        
        # 3. MOCK DATA (Varying numbers to prove it's alive)
        mock_price = round(random.uniform(0.10, 0.95), 2)
        mock_spread = random.choice([0.01, 0.02, 0.05, 0.10])
        mock_volume = round(random.uniform(1.0, 99.0), 1) # This MUST change every second

        results.append({
            'Ticker': ticker,
            'Score': score,
            'Status': '🔥 ACTIVE' if is_active else '🔎 SCANNING',
            'Option_Price': mock_price,
            'Spread': mock_spread,
            'Volume_M': mock_volume
        })
    
    # DEBUG: This will print in your Codespace terminal so you can see it working
    print(f"Data fetched at {time.strftime('%H:%M:%S')}")
    return pd.DataFrame(results)
