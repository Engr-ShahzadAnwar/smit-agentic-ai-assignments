"""
Chatbot Engine for Paulo - Broadway Pizza Waiter
Handles conversation logic using Google Gemini AI
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()


class PauloChatbot:
    def __init__(self):
        """Initialize Paulo chatbot with menu knowledge and system prompt"""
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Load menu knowledge base
        self.menu = self._load_menu()
        
        # Load Paulo's system prompt
        self.system_prompt = self._load_system_prompt()
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Add initial context with menu knowledge
        self._initialize_context()
    
    def _load_menu(self) -> Dict:
        """Load the Broadway Pizza menu from JSON file"""
        try:
            menu_path = os.path.join(os.path.dirname(__file__), "broadway_menu.json")
            with open(menu_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading menu: {e}")
            return {}
    
    def _load_system_prompt(self) -> str:
        """Load Paulo's system prompt"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "paulo_system_prompt.txt")
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            return "You are Paulo, a friendly pizza waiter at Broadway Pizza."
    
    def _initialize_context(self):
        """Initialize conversation with system prompt and menu knowledge"""
        # Create menu summary for context
        menu_summary = self._create_menu_summary()
        
        # Initial system message
        initial_context = f"""{self.system_prompt}

=== MENU KNOWLEDGE BASE ===
{menu_summary}

Remember: You are Paulo, and this is your complete menu knowledge. Never invent items or prices not listed here.
"""
        self.conversation_history.append({
            "role": "user",
            "parts": [initial_context]
        })
        self.conversation_history.append({
            "role": "model",
            "parts": ["Understood! I'm Paulo, the friendly waiter at Broadway Pizza. I'm ready to help customers with our delicious menu! 🍕"]
        })
    
    def _create_menu_summary(self) -> str:
        """Create a formatted menu summary for AI context"""
        summary = []
        
        # Restaurant info
        if "restaurant_info" in self.menu:
            info = self.menu["restaurant_info"]
            summary.append(f"Restaurant: {info.get('name', 'Broadway Pizza')}")
            summary.append(f"Hours: {info.get('delivery_hours', 'N/A')}")
            summary.append(f"Delivery Fee: Rs. {info.get('delivery_fee', 150)}")
            summary.append(f"Minimum Order: Rs. {info.get('minimum_order', 500)}\n")
        
        # Pizzas
        if "pizzas" in self.menu and "gourmet_flavors" in self.menu["pizzas"]:
            summary.append("GOURMET PIZZAS:")
            for pizza in self.menu["pizzas"]["gourmet_flavors"]:
                summary.append(f"- {pizza['name']}: {pizza['description']}")
                prices = pizza.get('prices', {})
                summary.append(f"  Small: Rs. {prices.get('small', 0)}, Medium: Rs. {prices.get('medium', 0)}, Large: Rs. {prices.get('large', 0)}, X-Large: Rs. {prices.get('xlarge', 0)}")
            summary.append("")
        
        # Deals
        if "deals" in self.menu:
            for deal_type, deals in self.menu["deals"].items():
                summary.append(f"{deal_type.upper().replace('_', ' ')}:")
                for deal in deals:
                    summary.append(f"- {deal['name']}: {deal['description']} - Rs. {deal['price']}")
                summary.append("")
        
        # Appetizers
        if "appetizers" in self.menu:
            summary.append("APPETIZERS:")
            for app in self.menu["appetizers"]:
                summary.append(f"- {app['name']}: {app['description']} - Rs. {app['price']}")
            summary.append("")
        
        # Pastas
        if "pastas" in self.menu:
            summary.append("PASTAS:")
            for pasta in self.menu["pastas"]:
                summary.append(f"- {pasta['name']}: {pasta['description']} - Rs. {pasta['price']}")
            summary.append("")
        
        # Desserts
        if "desserts" in self.menu:
            summary.append("DESSERTS:")
            for dessert in self.menu["desserts"]:
                summary.append(f"- {dessert['name']}: {dessert['description']} - Rs. {dessert['price']}")
            summary.append("")
        
        # Drinks
        if "drinks" in self.menu:
            summary.append("DRINKS:")
            for drink in self.menu["drinks"]:
                summary.append(f"- {drink['name']}: {', '.join([f'{size}: Rs. {price}' for size, price in drink.get('sizes', {}).items()])}")
            summary.append("")
        
        # Dips
        if "dips" in self.menu:
            summary.append("DIPS:")
            for dip in self.menu["dips"]:
                summary.append(f"- {dip['name']}: Rs. {dip['price']}")
            summary.append("")
        
        return "\n".join(summary)
    
    def chat(self, user_message: str, order_context: str = "") -> str:
        """
        Process user message and generate Paulo's response
        
        Args:
            user_message: The user's message
            order_context: Current order summary for context
        
        Returns:
            Paulo's response
        """
        try:
            # Add order context if available
            context_message = user_message
            if order_context:
                context_message = f"[Current Order Status: {order_context}]\n\nCustomer: {user_message}"
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "parts": [context_message]
            })
            
            # Generate response
            chat = self.model.start_chat(history=self.conversation_history[:-1])
            response = chat.send_message(context_message)
            
            # Add response to history
            self.conversation_history.append({
                "role": "model",
                "parts": [response.text]
            })
            
            return response.text
        
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I apologize, I'm having trouble processing your request. Please try again, or you can call us at 111-339-339 for assistance! 🍕"
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        self._initialize_context()
    
    def get_greeting(self) -> str:
        """Get Paulo's opening greeting"""
        return "Hi there! Welcome to Broadway Pizza 🍕\nWhat can I get started for you today?"
