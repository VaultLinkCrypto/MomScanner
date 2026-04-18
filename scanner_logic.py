from tradier_client import TradierClient
from engine import MomentumEngine

def run_funnel():
    tradier = TradierClient()
    engine = MomentumEngine()
    
    # 1. Start with a "Watchlist" of high-volume tickers 
    # (Scanning 11k every second is impossible, so we focus on the top 100-200)
    watchlist = ["TSLA", "NVDA", "AAPL", "AMD", "MSFT", "META", "AMZN", "GOOGL"]
    
    raw_quotes = tradier.get_market_quotes(watchlist)
    
    final_candidates = []
    for q in raw_quotes:
        # Filter 1: Volume must be high
        if q['volume'] < 500000: continue
        
        # Filter 2: Calculate Momentum Score
        # (For L1 data, we use price velocity as a proxy for raw_value)
        change_pct = q['change_percentage']
        score = engine.update_score(q['symbol'], 50 + (change_pct * 5))
        
        final_candidates.append({
            'Ticker': q['symbol'],
            'Price': q['last'],
            'Score': score,
            'Volume': q['volume']
        })
        
    return pd.DataFrame(final_candidates)
