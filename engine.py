class MomentumEngine:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.scores = {}

    def calculate_score(self, ticker, l2_data):
        # 1. Calculate Order Book Imbalance (Raw Value)
        bid_vol = sum([b['size'] for b in l2_data.get('bids', [])])
        ask_vol = sum([a['size'] for a in l2_data.get('asks', [])])
        
        if (bid_vol + ask_vol) == 0: return 50.0
        
        raw_ratio = (bid_vol - ask_vol) / (bid_vol + ask_vol)
        raw_score = ((raw_ratio + 1) / 2) * 100
        
        # 2. Apply Exponential Smoothing (The 'Brake Pedal')
        prev_score = self.scores.get(ticker, 50.0)
        smoothed_score = (raw_score * self.alpha) + (prev_score * (1 - self.alpha))
        
        self.scores[ticker] = smoothed_score
        return round(smoothed_score, 2)
