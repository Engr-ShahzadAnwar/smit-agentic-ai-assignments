import urllib.request
import json
import time

class FreeCryptoAPIClient:
    def __init__(self, base_url="https://freecryptoapi.com"):
        self.base_url = base_url

    def fetch_coin_data(self, coin_name):
        """
        Fetch coin data from the FreeCryptoAPI.
        Returns dict or None if failed/not found.
        """
        # Note: This is a hypothetical endpoint based on the prompt.
        url = f"{self.base_url}/coins/{coin_name.lower()}"
        
        try:
            # simple GET request with timeout
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    return data
                else:
                    return None
        except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
            # Network error or timeout or 404
            return None
