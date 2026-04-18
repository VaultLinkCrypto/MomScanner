import pandas as pd
from engine import MomentumEngine
from mock_data import get_mock_l2
import random

# We initialize the engine ONCE so it keeps its memory
if 'engine_instance' not in globals():
    engine_instance = MomentumEngine(alpha=0.2)

def run_funnel(watchlist):
    results = []
    
    # 1. Scan the whole watchlist (The Lake)
    for ticker in watchlist:
        l2_data = get_mock_l2(ticker) # Mocking L2
        score = engine_instance.calculate_score(ticker, l2_data)
        
        # 2. Only return data if the Ticker is in the "VIP Lounge"
        if ticker in engine_instance.active_tickers:
            results.append({
                'Ticker': ticker,
                'Score': score,
                'Option_Price': round(random.uniform(0.10, 0.90), 2),
                'Spread': random.choice([0.01, 0.02, 0.05]),
                'Status': 'STABLE MOVE' if score > 50 else 'WEAKENING'
            })
            
    return pd.DataFrame(results)
