class MomentumEngine:
    def __init__(self, alpha=0.1): # Lower alpha = even more stability
        self.alpha = alpha
        self.scores = {}
        self.active_tickers = set()
        self.ENTRY_BAR = 80
        self.EXIT_BAR = 40

    def calculate_score(self, ticker, l2_data):
        # 1. Calculate Raw Order Flow
        bid_vol = sum([b['size'] for b in l2_data.get('bids', [])])
        ask_vol = sum([a['size'] for a in l2_data.get('asks', [])])
        
        raw_score = 50.0
        if (bid_vol + ask_vol) > 0:
            ratio = (bid_vol - ask_vol) / (bid_vol + ask_vol)
            raw_score = ((ratio + 1) / 2) * 100
        
        # 2. Smooth the Score (EMA)
        prev_score = self.scores.get(ticker, 50.0)
        smoothed_score = (raw_score * self.alpha) + (prev_score * (1 - self.alpha))
        self.scores[ticker] = smoothed_score
        
        # 3. Status Logic (Does not delete, just labels)
        if smoothed_score >= self.ENTRY_BAR:
            self.active_tickers.add(ticker)
        elif smoothed_score < self.EXIT_BAR:
            if ticker in self.active_tickers:
                self.active_tickers.remove(ticker)
        
        return round(smoothed_score, 2)
