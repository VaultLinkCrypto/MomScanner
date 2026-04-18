import os
import requests

class TradierClient:
    def __init__(self):
        self.token = os.getenv('TRADIER_TOKEN')
        self.base_url = "https://api.tradier.com/v1/"
        self.headers = {'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}

    def get_market_quotes(self, symbols):
        """Fetches Level 1 data for a list of symbols (The Broad Net)."""
        url = f"{self.base_url}markets/quotes"
        params = {'symbols': ','.join(symbols)}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json().get('quotes', {}).get('quote', [])

    def get_level2_book(self, symbol):
        """Fetches the Order Book (The Sniper View)."""
        # Note: Requires the L2 upgrade to be active
        url = f"{self.base_url}markets/events/session" # Simplified for session init
        # Once L2 is live, this will use the websocket or book endpoint
        return requests.get(url, headers=self.headers).json()
