# 🌤️ Weather Chatbot with Function Calling

A smart AI assistant that combines natural conversation with real-time weather data fetching. Built with **Streamlit**, **Google Gemini AI**, and **OpenWeatherMap**.

## 🌟 Features

*   **🧠 Intelligent Conversation**: Powered by Google's Gemini Pro model for natural interactions.
*   **⚡ Function Calling**: Automatically detects when to call external APIs (like weather) based on your questions.
*   **🌍 Real-Time Weather**: Fetches accurate, up-to-the-minute weather data for any city globally.
*   **🎨 Glassmorphism UI**: specific, modern interface designed for a premium user experience.
*   **📝 Conversation History**: Keeps track of your chat so you can ask follow-up questions.
*   **🕵️ Transparent Logic**: Visual indicators show exactly when the AI is using a tool vs. just chatting.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8 to 3.12**: [Download Python](https://www.python.org/downloads/)
*   **Git** (Optional, for cloning): [Download Git](https://git-scm.com/downloads)

You will also need API keys for:
1.  **Google Gemini AI**: [Get API Key](https://aistudio.google.com/app/apikey)
2.  **OpenWeatherMap**: [Get API Key](https://home.openweathermap.org/api_keys)

---

## 🚀 Installation & Setup Guide

Follow these steps to set up the project locally.

### 1. Clone or Download the Project
If you have Git installed:
```bash
git clone <repository_url>
cd weather_chatbot
```
*Or download the ZIP file and extract it to a folder.*

### 2. Create a Virtual Environment (Recommended)
A virtual environment keeps your project dependencies isolated.

**On Windows:**
```powershell
# Create the virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```
*You should see `(venv)` appear at the start of your terminal line.*

### 3. Install Dependencies
With your virtual environment activated, install the required libraries:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1.  Look for a file named `.env.example` in the project folder.
2.  Duplicate it and rename the copy to `.env`.
3.  Open `.env` in a text editor (Notepad, VS Code, etc.) and paste your API keys:

```ini
GEMINI_API_KEY=AIzaSy...your_gemini_key_here
WEATHER_API_KEY=a1b2c3...your_openweathermap_key_here
```
*(Make sure there are no spaces or quotes around the keys)*

---

## ▶️ How to Run

1.  Make sure your virtual environment is still activated (you see `(venv)`).
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.   The app should automatically open in your browser at `http://localhost:8501`.

---

## 📖 User Guide

### The Interface
*   **Chat Input**: Located at the bottom. Type your messages here.
*   **Chat History**: The main area displays the conversation bubbles.
*   **Sidebar**: Contains settings or "About" information (if configured).

### How to Interact

**1. Ask about the Weather (Triggers Function Calling)**
When you ask for weather, the AI "calls" the weather tool behind the scenes.
*   *"What is the weather in Tokyo?"*
*   *"Is it raining in London right now?"*
*   *"Temperature in New York?"*

**2. General Conversation (Normal AI Chat)**
You can talk to it like a normal chatbot.
*   *"Tell me a joke."*
*   *"How does a rainbow form?"*
*   *"Write a short poem about rain."*

### Understanding the Output
*   **Bot Response**: The natural language answer from the AI.
*   **"Function Called" Badge**: If you see a small interactive element or badge saying a function was used, it means the AI fetched real data to answer you.

---

## 📂 Project Structure

```text
weather_chatbot/
├── app.py                 # Main application file (Streamlit UI)
├── chatbot_engine.py      # Logic for Gemini AI and function calling calls
├── weather_api.py         # Helper functions to talk to OpenWeatherMap
├── requirements.txt       # List of python libraries needed
├── .env                   # Your API keys (DO NOT SHARE THIS FILE)
└── README.md              # Documentation
```

## ❓ Troubleshooting

*   **Issue**: `ModuleNotFoundError`
    *   **Fix**: Ensure you activated your virtual environment (`venv`) before running the app.
*   **Issue**: `API Key Error`
    *   **Fix**: Double-check your `.env` file. Ensure variable names are exactly `GEMINI_API_KEY` and `WEATHER_API_KEY`.
*   **Issue**: "City not found"
    *   **Fix**: Try typing the city name correctly or adding the country code (e.g., "Paris, FR").

---
*Created for the AI Agentic Class Project.*
