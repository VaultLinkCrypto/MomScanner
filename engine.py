class MomentumEngine:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.scores = {}
        self.active_tickers = set()  # The "VIP Lounge"
        
        # Hysteresis Thresholds
        self.ENTRY_BAR = 80  # Hard to get in
        self.EXIT_BAR = 40   # Hard to get kicked out

    def calculate_score(self, ticker, l2_data):
        # ... (Existing EMA math from previous step) ...
        bid_vol = sum([b['size'] for b in l2_data.get('bids', [])])
        ask_vol = sum([a['size'] for a in l2_data.get('asks', [])])
        
        if (bid_vol + ask_vol) == 0: raw_score = 50.0
        else:
            raw_ratio = (bid_vol - ask_vol) / (bid_vol + ask_vol)
            raw_score = ((raw_ratio + 1) / 2) * 100
        
        prev_score = self.scores.get(ticker, 50.0)
        smoothed_score = (raw_score * self.alpha) + (prev_score * (1 - self.alpha))
        self.scores[ticker] = smoothed_score
        
        # --- NEW HYSTERESIS LOGIC ---
        # 1. Promote to Active if it hits the Entry Bar
        if smoothed_score >= self.ENTRY_BAR:
            self.active_tickers.add(ticker)
            
        # 2. Kick out only if it drops below the Exit Bar
        elif smoothed_score < self.EXIT_BAR:
            if ticker in self.active_tickers:
                self.active_tickers.remove(ticker)
        
        return round(smoothed_score, 2)
