import random

def get_mock_l2(symbol):
    """Generates a fake Level 2 order book for testing."""
    price = random.uniform(150, 200)
    
    # Simulate a 'Buy Wall' (BULLISH) for TSLA and NVDA
    if symbol in ['TSLA', 'NVDA']:
        bids = [{'price': price - 0.01, 'size': random.randint(500, 1000)} for _ in range(5)]
        asks = [{'price': price + 0.01, 'size': random.randint(10, 50)} for _ in range(5)]
    else:
        # Balanced or Bearish for others
        bids = [{'price': price - 0.01, 'size': random.randint(10, 100)} for _ in range(5)]
        asks = [{'price': price + 0.01, 'size': random.randint(100, 500)} for _ in range(5)]
        
    return {'bids': bids, 'asks': asks}
