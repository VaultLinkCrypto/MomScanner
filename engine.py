import pandas as pd

class MomentumEngine:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.scores = {} # Stores {ticker: current_ema_score}

    def update_score(self, ticker, raw_value):
        """Calculates the smoothed score to prevent 'flickering'."""
        prev_score = self.scores.get(ticker, 50.0) # Default to neutral
        new_score = (raw_value * self.alpha) + (prev_score * (1 - self.alpha))
        self.scores[ticker] = new_score
        return round(new_score, 2)

    def calculate_imbalance(self, l2_data):
        """Calculates Buy/Sell pressure from Level 2 data."""
        # Placeholder logic for L2 data structure
        bids = sum([b['size'] for b in l2_data.get('bids', [])])
        asks = sum([a['size'] for a in l2_data.get('asks', [])])
        
        if (bids + asks) == 0: return 50
        ratio = (bids - asks) / (bids + asks)
        return ((ratio + 1) / 2) * 100
