def run_funnel(watchlist):
    results = []
    for ticker in watchlist:
        # (Mock or Live Logic here)
        score = engine.calculate_score(ticker, get_mock_l2(ticker))
        
        results.append({
            'Ticker': ticker, # This 'Ticker' key MUST match the master_df
            'Score': score,
            'Option_Price': round(random.uniform(0.10, 0.90), 2),
            'Spread': random.choice([0.01, 0.02, 0.05])
        })
    return pd.DataFrame(results)
