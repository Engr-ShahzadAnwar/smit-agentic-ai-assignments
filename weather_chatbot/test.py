import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content("Hello, can you hear me?")
    print("Success! Model response:")
    print(response.text)
except Exception as e:
    print(f"Error connecting to Gemini: {e}")