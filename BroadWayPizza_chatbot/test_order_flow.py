"""
Test script for Broadway Pizza Chatbot Order Flow
Tests the complete order-taking process with new system prompt rules
"""

import os
from chatbot_engine import PauloChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_separator():
    print("\n" + "="*80 + "\n")

def test_complete_order_flow():
    """Test the complete order flow from greeting to JSON output"""
    
    print("🍕 BROADWAY PIZZA CHATBOT - ORDER FLOW TEST")
    print_separator()
    
    # Initialize chatbot
    try:
        chatbot = PauloChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    print_separator()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Complete Order Flow",
            "messages": [
                "Hi, I want to order pizza",
                "I want Dancing Fajita",
                "Large size",
                "Just one",
                "Regular crust please",
                "Yes, add a 1.5L drink",
                "Yes, that's all",
                "Yes, confirm the order",
                "Delivery please",
                "Cash on Delivery",
                "Ahmed Khan",
                "0300-1234567",
                "House 123, Street 5, DHA Phase 2, Karachi"
            ]
        },
        {
            "name": "Item Not Available",
            "messages": [
                "Do you have burgers?",
            ]
        },
        {
            "name": "Order Cancellation",
            "messages": [
                "I want to cancel my order",
                "Order ORD-20260127-001",
                "Yes, cancel it"
            ]
        },
        {
            "name": "Menu Inquiry",
            "messages": [
                "What are your bestsellers?",
                "Show me the deals"
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"📋 TEST SCENARIO: {scenario['name']}")
        print_separator()
        
        # Reset conversation for each scenario
        chatbot.reset_conversation()
        
        # Get greeting
        greeting = chatbot.get_greeting()
        print(f"🤖 Paulo: {greeting}")
        print()
        
        # Process each message
        for i, user_message in enumerate(scenario['messages'], 1):
            print(f"👤 Customer ({i}): {user_message}")
            
            try:
                response = chatbot.chat(user_message)
                print(f"🤖 Paulo: {response}")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        print_separator()
        input("Press Enter to continue to next scenario...")
        print_separator()

def test_appetizing_descriptions():
    """Test if chatbot uses appetizing language for food descriptions"""
    
    print("🍕 TESTING APPETIZING LANGUAGE")
    print_separator()
    
    chatbot = PauloChatbot()
    
    test_queries = [
        "Tell me about the Dancing Fajita pizza",
        "What's in the Tarzan Tikka?",
        "Describe your Chocolate Lava Cake"
    ]
    
    for query in test_queries:
        print(f"👤 Customer: {query}")
        response = chatbot.chat(query)
        print(f"🤖 Paulo: {response}")
        print()
    
    print_separator()

def test_order_summary_format():
    """Test if order summary follows the required format"""
    
    print("🍕 TESTING ORDER SUMMARY FORMAT")
    print_separator()
    
    chatbot = PauloChatbot()
    
    messages = [
        "I want 2 large Dancing Fajita pizzas",
        "Regular crust",
        "Add garlic bread",
        "That's all"
    ]
    
    for msg in messages:
        print(f"👤 Customer: {msg}")
        response = chatbot.chat(msg)
        print(f"🤖 Paulo: {response}")
        print()
    
    print_separator()

def main():
    """Run all tests"""
    
    print("\n" + "🍕"*40)
    print("BROADWAY PIZZA CHATBOT - COMPREHENSIVE TEST SUITE")
    print("🍕"*40 + "\n")
    
    tests = [
        ("Complete Order Flow", test_complete_order_flow),
        ("Appetizing Descriptions", test_appetizing_descriptions),
        ("Order Summary Format", test_order_summary_format)
    ]
    
    print("Available Tests:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"{i}. {name}")
    print(f"{len(tests) + 1}. Run All Tests")
    print()
    
    choice = input("Select test to run (1-{}): ".format(len(tests) + 1))
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(tests):
            print_separator()
            tests[choice_num - 1][1]()
        elif choice_num == len(tests) + 1:
            for name, test_func in tests:
                print_separator()
                test_func()
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    main()
