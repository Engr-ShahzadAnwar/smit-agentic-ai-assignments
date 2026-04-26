"""
Quick test script to verify Paulo chatbot is working
"""

from chatbot_engine import PauloChatbot
from order_manager import OrderManager

def test_chatbot():
    print("🍕 Testing Paulo Chatbot...\n")
    
    try:
        # Initialize chatbot
        print("1. Initializing Paulo...")
        chatbot = PauloChatbot()
        order_manager = OrderManager()
        print("✅ Paulo initialized successfully!\n")
        
        # Test greeting
        print("2. Testing greeting...")
        greeting = chatbot.get_greeting()
        print(f"Paulo says: {greeting}\n")
        
        # Test menu query
        print("3. Testing menu query...")
        response = chatbot.chat("What pizzas do you have?")
        print(f"Paulo says: {response}\n")
        
        # Test order management
        print("4. Testing order management...")
        order_manager.create_new_order()
        order_manager.add_item("Large Dancing Fajita Pizza", 1299, 1, {"crust": "Regular"})
        order_manager.add_item("Garlic Bread", 399, 1)
        print(order_manager.get_order_summary())
        
        print("\n✅ All tests passed! Paulo is ready to serve! 🍕")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your GEMINI_API_KEY")
        print("2. Installed all requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    test_chatbot()
