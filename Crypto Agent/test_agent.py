import unittest
from unittest.mock import MagicMock
from agent import CryptoAgent
import time
from datetime import datetime, timedelta

class TestCryptoAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CryptoAgent()
        # Reset KB for testing without overwriting file permanently? 
        # Ideally we mock KBManager, but let's just mock the internal data for now
        # or rely on the file but assume it has the default data I wrote.
        
        # Mock API Client to avoid real network calls
        self.agent.api_client.fetch_coin_data = MagicMock(return_value=None)

    def test_kb_hit_metadata(self):
        # Bitcoin is in the initial JSON
        response = self.agent.process_query("Tell me about Bitcoin")
        self.assertIn("Bitcoin", response["answer"])
        self.assertIn("Launch Year", response["answer"] if "Launch Year" in response["answer"] else "launched in")
        self.assertEqual(response["source"], "Knowledge Base")

    def test_kb_hit_price(self):
        response = self.agent.process_query("What is the price of Ethereum?")
        self.assertIn("3000", response["answer"])
        self.assertEqual(response["source"], "Knowledge Base")

    def test_context_resolution(self):
        self.agent.process_query("Tell me about Solana")
        response = self.agent.process_query("What is its consensus?")
        self.assertIn("Proof of History", response["answer"])
        self.assertEqual(response["source"], "Knowledge Base")

    def test_disallowed_query(self):
        response = self.agent.process_query("Will Bitcoin price go up?")
        self.assertEqual(response["answer"], "INSUFFICIENT DATA – Not found in Knowledge Base or API") 
        # Note: My implementation returns the exact rejection string.

    def test_api_call_on_miss(self):
        # Query for unknown coin -> triggers API
        # Mock API success
        self.agent.api_client.fetch_coin_data = MagicMock(return_value={
            "name": "Dogecoin",
            "symbol": "DOGE",
            "price": 0.1,
            "market_cap": 10000000,
            "last_updated": datetime.now().isoformat()
        })
        
        response = self.agent.process_query("What is the price of Dogecoin?")
        self.agent.api_client.fetch_coin_data.assert_called()
        self.assertIn("0.1", response["answer"])
        self.assertEqual(response["source"], "FreeCryptoAPI")
        self.assertEqual(response["confidence"], 1.0)

    def test_rejection_no_data(self):
        # Unknown coin, API fails
        self.agent.api_client.fetch_coin_data = MagicMock(return_value=None)
        response = self.agent.process_query("What is the price of FakeCoin?")
        self.assertEqual(response["answer"], "INSUFFICIENT DATA – Not found in Knowledge Base or API")

if __name__ == '__main__':
    unittest.main()
