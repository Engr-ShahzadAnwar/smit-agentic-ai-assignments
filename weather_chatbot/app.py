import streamlit as st
from chatbot_engine import ChatbotEngine

# Page configuration
st.set_page_config(
    page_title="Weather Chatbot",
    page_icon="🌤️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #4CAF50;
    }
    .assistant-message {
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-left: 4px solid #2196F3;
    }
    .function-call-badge {
        display: inline-block;
        background-color: #FF9800;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    h1 {
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "function_calls" not in st.session_state:
    st.session_state.function_calls = []

# Title and description
st.title("🌤️ Weather Chatbot")
st.markdown('<p class="subtitle">Ask me about the weather in any city!</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This chatbot uses **function calling** to fetch real-time weather data.
    
    **Try asking:**
    - "What's the weather in London?"
    - "How's the temperature in Tokyo?"
    - "Tell me about the weather in Paris"
    - "Is it raining in New York?"
    
    You can also have general conversations!
    """)
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.session_state.function_calls = []
        st.session_state.chatbot.reset_chat()
        st.rerun()

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        function_badge = ""
        if idx < len(st.session_state.function_calls) and st.session_state.function_calls[idx]:
            function_badge = '<span class="function-call-badge">🔧 Function Called: get_weather()</span>'
        
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {content}
                {function_badge}
            </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me about the weather..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get chatbot response
    with st.spinner("🤔 Thinking..."):
        response, function_called = st.session_state.chatbot.process_message(prompt)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.function_calls.append(function_called)
    
    # Rerun to display new messages
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">Powered by Gemini AI & OpenWeatherMap</p>',
    unsafe_allow_html=True
)
