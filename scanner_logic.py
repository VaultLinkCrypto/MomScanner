import pandas as pd
from mock_data import get_mock_l2
import random

def run_funnel(watchlist, engine): # Now accepts 'engine' as a variable
    results = []
    
    for ticker in watchlist:
        # Get the mock data
        l2_data = get_mock_l2(ticker)
        
        # Calculate the score using the PERSISTENT engine
        score = engine.calculate_score(ticker, l2_data)
        
        # Determine Status
        status = 'ACTIVE' if ticker in engine.active_tickers else 'SCANNING'
        
        results.append({
            'Ticker': ticker,
            'Score': score,
            'Status': status,
            'Option_Price': round(random.uniform(0.10, 0.90), 2),
            'Spread': random.choice([0.01, 0.02, 0.05])
        })
        
    return pd.DataFrame(results)
