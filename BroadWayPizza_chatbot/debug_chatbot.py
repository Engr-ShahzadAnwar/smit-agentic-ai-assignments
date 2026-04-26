from chatbot_engine import PauloChatbot
import os
from dotenv import load_dotenv

# Force reload of environment variables
load_dotenv()

print(f"Checking API Key presence: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

try:
    bot = PauloChatbot()
    print("Chatbot initialized successfully.")
    response = bot.chat("Hello, what is on the menu?")
    print(f"Response: {response}")
except Exception as e:
    print(f"CRITICAL ERROR CAUGHT: {e}")
