import re
from kb_manager import KBManager
from api_client import FreeCryptoAPIClient

class CryptoAgent:
    def __init__(self):
        self.kb_manager = KBManager()
        self.api_client = FreeCryptoAPIClient()
        self.history = [] # List of {'role':, 'content':}
        self.max_history = 10

    def _add_to_history(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def _detect_entity(self, query):
        """
        Identify coin name or symbol from query.
        Uses a simple list of known coins for now, plus history context.
        """
        # Simple extraction - this could be improved with NLP
        # Check for known coins in KB first
        tokens = query.lower().split()
        
        # Hardcoded common coins for detection if not in KB yet, or check typical patterns
        # In a real agent, this would be more robust.
        # Check against KB keys
        known_coins = list(self.kb_manager.data.get("coins", {}).keys())
        # Also map symbols to keys?
        
        # Check for symbols in KB
        for key, data in self.kb_manager.data.get("coins", {}).items():
            if data["symbol"].lower() in tokens:
                return key
            if key in tokens:
                return key
        
        # Check context if 'it', 'this', 'the coin' is used
        if any(w in tokens for w in ['it', 'its', 'this', 'that']):
            # Look back in history for the last mentioned entity
            for turn in reversed(self.history):
                if turn['role'] == 'user':
                    # Try to find entity in previous user msg? 
                    # Often better to find what the *agent* talked about or the verified entity
                    pass
                if 'entity' in turn: # If we stored metadata
                   return turn['entity']

        # Fallback: naive heuristic (e.g. capitalized words in original query? regex?)
        # For this assignment, we expect the user to name the coin or refer to it.
        # Let's try to grab potential coin names (alphanumeric)
        return None

    def _detect_intent(self, query):
        query = query.lower()
        if any(w in query for w in ["price", "value", "cost", "worth"]):
            return "price"
        if any(w in query for w in ["market cap", "marketcap", "capitalization"]):
            return "market_cap"
        if any(w in query for w in ["consensus", "proof", "mechanism"]):
            return "consensus"
        if any(w in query for w in ["chain", "type", "network"]):
            return "chain_type"
        if any(w in query for w in ["launch", "year", "founded", "started"]):
            return "launch_year"
        if any(w in query for w in ["predict", "prediction", "forecast", "future", "buy", "sell", "investment", "trade"]):
            return "disallowed"
        return "metadata" # Default fallback for "Tell me about..."

    def _reject(self):
        return {
            "answer": "INSUFFICIENT DATA – Not found in Knowledge Base or API",
            "source": None,
            "confidence": 0.0
        }

    def process_query(self, user_query):
        # 1. Update History
        self._add_to_history("user", user_query)
        
        # 2. Check Disallowed
        intent = self._detect_intent(user_query)
        if intent == "disallowed":
            # Strict rejection for opinions/predictions
            # The prompt says "INSUFFICIENT DATA" for "Not found in KB or API".
            # It also says "DISALLOWED QUERIES... Price prediction... REJECT".
            # But the rejection message "INSUFFICIENT DATA" seems specific to data lookup failure.
            # However, under "FINAL ENFORCEMENT... If a single rule is violated... ONLY reject using the defined rejection message".
            # So I must use "INSUFFICIENT DATA..." even for opinions?
            # Re-reading: "Rejection Message (EXACT): INSUFFICIENT DATA – Not found in Knowledge Base or API"
            # This specific message implies data absence. 
            # But "DISALLOWED QUERIES" section says "Price prediction... Investment advice... Any data not present in KB or API".
            # Asking for a prediction is asking for data NOT in KB/API. So yes.
            response = self._reject()
            self._add_to_history("agent", response["answer"])
            return response

        # 3. Detect Entity
        entity = self._detect_entity(user_query)
        # Context resolution
        if not entity:
            # Check history references
            last_entity = self._get_context_entity()
            if last_entity:
                entity = last_entity
        
        if not entity:
             # Cannot answer without entity
            response = self._reject()
            self._add_to_history("agent", response["answer"])
            return response

        # Store entity context for this turn
        self.history[-1]['entity'] = entity

        # 4. Search KB
        data, is_fresh = self.kb_manager.get_coin_data(entity)

        answer_source = None
        final_answer = ""
        confidence = 0.0

        # Logic: 
        # Is data sufficient (exists) AND fresh?
        # YES -> Answer KB
        # NO -> Call API
        
        fetched_from_api = False
        if not data or not is_fresh:
            # Call API
            api_data = self.api_client.fetch_coin_data(entity)
            if api_data:
                # Update KB
                self.kb_manager.update_coin_data(entity, api_data)
                data = api_data # use new data
                is_fresh = True
                fetched_from_api = True
                answer_source = "FreeCryptoAPI"
                confidence = 1.0
            else:
                # API Failed. 
                # If we have stale data, do we use it?
                # "If fact not in KB AND not returned by API -> REJECT"
                # If it IS in KB (stale), we might use it?
                # But freshness rule "Use API ONLY IF... Cached data is older" implies we want fresh data.
                # If API fails, usually we fallback to stale data with lower confidence.
                if data:
                     answer_source = "Knowledge Base" # Fallback
                     confidence = 0.5 # Stale
                else:
                    response = self._reject()
                    self._add_to_history("agent", response["answer"])
                    return response
        else:
             # Data exists and is fresh
             answer_source = "Knowledge Base"
             confidence = 1.0

        # 5. Formulate Answer
        if intent == "metadata":
             final_answer = f"{data.get('name', entity)} ({data.get('symbol', 'N/A')}) was launched in {data.get('launch_year', 'N/A')}."
        elif intent == "price":
             final_answer = f"The price of {data.get('name', entity)} is ${data.get('price', 'N/A')}."
        elif intent == "market_cap":
             final_answer = f"The market cap of {data.get('name', entity)} is ${data.get('market_cap', 'N/A')}."
        elif intent == "consensus":
             final_answer = f"The consensus mechanism of {data.get('name', entity)} is {data.get('consensus_mechanism', 'N/A')}."
        elif intent == "chain_type":
             final_answer = f"The chain type of {data.get('name', entity)} is {data.get('chain_type', 'N/A')}."
        else:
             # Generic fallback
             final_answer = f"Data for {entity}: {data}"

        response_text = f"Answer: {final_answer}\nSource: {answer_source}\nConfidence: {confidence}"
        
        self._add_to_history("agent", response_text)
        self.history[-1]['entity'] = entity # Update agent turn with entity too for robustness?

        return {
            "answer": final_answer,
            "source": answer_source,
            "confidence": confidence,
            "formatted": response_text
        }

    def _get_context_entity(self):
        # Look back for the last identified entity
        for turn in reversed(self.history[:-1]): # Skip current turn
             if 'entity' in turn:
                 return turn['entity']
        return None
