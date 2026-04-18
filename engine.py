class MomentumEngine:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.scores = {}
        self.active_tickers = set()
        self.ENTRY_BAR = 80
        self.EXIT_BAR = 40

    def calculate_score(self, ticker, l2_data):
        # Sum up volumes from the mock data
        bid_vol = sum([b['size'] for b in l2_data.get('bids', [])])
        ask_vol = sum([a['size'] for a in l2_data.get('asks', [])])
        
        raw_score = 50.0
        if (bid_vol + ask_vol) > 0:
            ratio = (bid_vol - ask_vol) / (bid_vol + ask_vol)
            raw_score = ((ratio + 1) / 2) * 100
        
        # EMA Smoothing
        prev_score = self.scores.get(ticker, 50.0)
        smoothed_score = (raw_score * self.alpha) + (prev_score * (1 - self.alpha))
        self.scores[ticker] = smoothed_score
        
        # Persistence Logic
        if smoothed_score >= self.ENTRY_BAR:
            self.active_tickers.add(ticker)
        elif smoothed_score < self.EXIT_BAR:
            if ticker in self.active_tickers:
                self.active_tickers.remove(ticker)
        
        return round(smoothed_score, 2)
