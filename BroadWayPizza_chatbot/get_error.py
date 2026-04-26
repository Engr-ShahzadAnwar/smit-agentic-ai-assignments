import sys
import os
from chatbot_engine import PauloChatbot

# Redirect stderr to a file with UTF-8 encoding
sys.stderr = open('error_log.txt', 'w', encoding='utf-8')
sys.stdout = open('output_log.txt', 'w', encoding='utf-8')

print("Starting specific error capture...")

try:
    bot = PauloChatbot()
    print("Bot initialized.")
    bot.chat("Hello")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR: {e}")

print("Done.")
