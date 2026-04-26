import json
import os
from datetime import datetime, timedelta

KB_FILE_PATH = "knowledge_base.json"
FRESHNESS_THRESHOLD_MINUTES = 5

class KBManager:
    def __init__(self, file_path=KB_FILE_PATH):
        self.file_path = file_path
        self.data = self._load_kb()

    def _load_kb(self):
        if not os.path.exists(self.file_path):
            return {"coins": {}}
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"coins": {}}

    def _save_kb(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_coin_data(self, coin_name_or_symbol):
        """
        Search for coin data in the KB.
        Returns tuple: (data, is_fresh)
        """
        coin_name_or_symbol = coin_name_or_symbol.lower()
        
        # Search by key (name) or symbol
        found_key = None
        for key, info in self.data.get("coins", {}).items():
            if key.lower() == coin_name_or_symbol or info.get("symbol", "").lower() == coin_name_or_symbol:
                found_key = key
                break
        
        if not found_key:
            return None, False

        coin_data = self.data["coins"][found_key]
        last_updated_str = coin_data.get("last_updated")
        
        if not last_updated_str:
            return coin_data, False

        try:
            last_updated = datetime.fromisoformat(last_updated_str)
            if datetime.now() - last_updated < timedelta(minutes=FRESHNESS_THRESHOLD_MINUTES):
                return coin_data, True
            else:
                return coin_data, False
        except ValueError:
            return coin_data, False

    def update_coin_data(self, coin_name, new_data):
        """
        Update or add coin data to the KB.
        """
        coin_name = coin_name.lower()
        if "coins" not in self.data:
            self.data["coins"] = {}
        
        if coin_name not in self.data["coins"]:
            self.data["coins"][coin_name] = {}

        # Update fields
        self.data["coins"][coin_name].update(new_data)
        self.data["coins"][coin_name]["last_updated"] = datetime.now().isoformat()
        
        self._save_kb()
