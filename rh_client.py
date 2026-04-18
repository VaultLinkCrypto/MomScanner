import os
import robin_stocks.robinhood as rh

class RobinhoodClient:
    def __init__(self):
        self.user = os.getenv('RH_USERNAME')
        self.password = os.getenv('RH_PASSWORD')
        # rh.login(self.user, self.password) # Uncomment once secrets are set

    def find_lottos(self, ticker, max_price=1.00):
        """Finds cheap call options with tight spreads."""
        # This fetches the nearest Friday expiration
        try:
            chains = rh.options.get_chains(ticker)
            expiry = chains['expiration_dates'][0]
            options = rh.options.find_options_by_expiration(ticker, expiry, 'call')
            
            lottos = []
            for opt in options:
                ask = float(opt['ask_price'])
                bid = float(opt['bid_price'])
                if 0.01 <= ask <= max_price:
                    lottos.append({
                        'strike': opt['strike_price'],
                        'ask': ask,
                        'spread': round(ask - bid, 3)
                    })
            return lottos
        except:
            return []
