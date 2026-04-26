"""
Broadway Pizza Chatbot - Premium Website UI
Main Application
"""

import streamlit as st
import os
import time
import json
import re
from chatbot_engine import PauloChatbot
from order_manager import OrderManager

# Page Config
st.set_page_config(
    page_title="Broadway Pizza | Premium Order",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# Initialize State
if "chatbot" not in st.session_state:
    st.session_state.chatbot = PauloChatbot()
    st.session_state.order_manager = OrderManager()
    st.session_state.messages = []
    st.session_state.first_message = True

# --- ASSETS & HELPERS ---
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_tag(img_path, class_name=""):
    if os.path.exists(img_path):
        base64_img = get_base64_of_bin_file(img_path)
        return f'<img src="data:image/png;base64,{base64_img}" class="{class_name}">'
    return ""

ASSETS_DIR = "assets"
HERO_IMG_1 = os.path.join(ASSETS_DIR, "hero_1.png")
HERO_IMG_2 = os.path.join(ASSETS_DIR, "hero_2.png")
LOGO_IMG = os.path.join(ASSETS_DIR, "logo.png")
PIZZA_IMG = os.path.join(ASSETS_DIR, "pizza_item.png")

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists(LOGO_IMG):
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                {get_img_tag(LOGO_IMG, "sidebar-logo")}
                <h2 style="color: #E31837; font-family: 'Oswald'; margin:0;">BROADWAY</h2>
                <h3 style="color: #FDB913; font-family: 'Oswald'; margin:0;">PIZZA</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🍔 MENU EXPLORER")
    
    # Expanded Categories for Grid Layout
    categories = [
        ("Pizza", "Show me pizzas", PIZZA_IMG),
        ("Appetizers", "Show me appetizers", HERO_IMG_1), # Placeholder
        ("Wings", "Show me wings", HERO_IMG_2), # Placeholder
        ("Calzones", "Show me calzones", PIZZA_IMG), # Placeholder
        ("Pastas", "Show me pastas", HERO_IMG_1), # Placeholder
        ("Kids Meal", "Show me kids meals", HERO_IMG_2), # Placeholder
        ("Desserts", "Show me desserts", PIZZA_IMG), # Placeholder
        ("Deals", "Show me deals", HERO_IMG_2),
    ]
    
    st.markdown("---")
    
    # 2-Column Grid Layout
    # Create pairs of categories
    rows = [categories[i:i+2] for i in range(0, len(categories), 2)]
    
    for row in rows:
        cols = st.columns(2)
        for i, (label, query, img) in enumerate(row):
            with cols[i]:
                # Image Display
                if os.path.exists(img):
                    st.image(img, use_container_width=True)
                else:
                    st.write("🍔")
                
                # Button Selection
                if st.button(label, key=f"nav_{label}", use_container_width=True):
                     st.session_state.messages.append({"role": "user", "content": query})
                     context = st.session_state.order_manager.get_order_summary() if st.session_state.order_manager.has_items() else ""
                     response = st.session_state.chatbot.chat(query, context)
                     st.session_state.messages.append({"role": "assistant", "content": response})
                     st.rerun()

    st.markdown("---")
    
    # Live Order Summary
    st.markdown("### 🛒 YOUR ORDER")
    if st.session_state.order_manager.has_items():
        summary = st.session_state.order_manager.get_order_summary()
        st.markdown(f'<div class="cart-panel">{summary}</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Checkout", use_container_width=True):
            res = st.session_state.order_manager.confirm_order()
            if res["success"]:
                st.balloons()
                st.success(res["message"])
        if c2.button("🗑️ Clear", use_container_width=True):
            st.session_state.order_manager.cancel_order()
            st.rerun()
    else:
        st.info("Your cart is empty. Hungry?")

# --- MAIN CONTENT ---

# 1. HERO CAROUSEL (CSS Animation with Base64 Images)
if os.path.exists(HERO_IMG_1) and os.path.exists(HERO_IMG_2):
    b64_hero1 = get_base64_of_bin_file(HERO_IMG_1)
    b64_hero2 = get_base64_of_bin_file(HERO_IMG_2)
    
    carousel_css = f"""
    <style>
        .hero-slider {{
            width: 100%;
            height: 400px;
            position: relative;
            overflow: hidden;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 30px;
        }}
        .hero-slide {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            background-size: cover;
            background-position: center;
            opacity: 0;
            animation: slideAnimation 12s infinite;
        }}
        .hero-slide:nth-child(1) {{
            background-image: url('data:image/png;base64,{b64_hero1}');
            animation-delay: 0s;
        }}
        .hero-slide:nth-child(2) {{
            background-image: url('data:image/png;base64,{b64_hero2}');
            animation-delay: 6s;
        }}
        .hero-content {{
            position: absolute;
            bottom: 40px;
            left: 40px;
            z-index: 2;
        }}
        .hero-title-text {{
            font-family: 'Oswald', sans-serif;
            font-size: 4rem;
            color: white;
            text-transform: uppercase;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
            line-height: 1;
        }}
        .hero-subtitle-text {{
            font-size: 1.5rem;
            color: #FDB913;
            font-weight: 600;
            margin-top: 10px;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
        }}
        @keyframes slideAnimation {{
            0% {{ opacity: 0; transform: scale(1.05); }}
            10% {{ opacity: 1; transform: scale(1); }}
            45% {{ opacity: 1; transform: scale(1); }}
            55% {{ opacity: 0; transform: scale(1.05); }}
            100% {{ opacity: 0; }}
        }}
        .overlay-gradient {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60%;
            background: linear-gradient(to top, rgba(15,15,15,0.95), transparent);
            z-index: 1;
        }}
    </style>
    <div class="hero-slider">
        <div class="hero-slide"></div>
        <div class="hero-slide"></div>
        <div class="overlay-gradient"></div>
        <div class="hero-content">
            <div class="hero-title-text">FRESH. CHEESY.<br>LEGENDARY.</div>
            <div class="hero-subtitle-text">WELCOME TO BROADWAY PIZZA</div>
        </div>
    </div>
    """
    st.markdown(carousel_css, unsafe_allow_html=True)
else:
    st.title("🍕 BROADWAY PIZZA")

# 2. CHAT INTERFACE
st.markdown("""
<div class="chat-header">
    <div style="text-align:center; padding: 20px 0; border-bottom: 2px solid #222; margin-bottom: 20px;">
        <h1 style="color:white; font-size: 2rem; margin:0;">PAULO</h1>
        <div style="color:#FDB913; letter-spacing: 2px; font-size: 0.9rem; font-weight:600;">YOUR BROADWAY PIZZA ASSISTANT 🍕</div>
    </div>
</div>
""", unsafe_allow_html=True)


chat_container = st.container()
with chat_container:
    if st.session_state.first_message and not st.session_state.messages:
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state.first_message = False

    for msg in st.session_state.messages:
        avatar = "🍕" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# Helper for typing animation
import time
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    context = st.session_state.order_manager.get_order_summary() if st.session_state.order_manager.has_items() else ""
    with st.chat_message("assistant", avatar="🍕"):
        # Custom loading spinner is handled by Streamlit's internal spinner, but we can make it feel smoother
        with st.spinner("Paulo is thinking..."):
            full_response = st.session_state.chatbot.chat(prompt, context)
            
        # Parse JSON from response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', full_response, re.DOTALL)
        display_response = full_response
        
        if json_match:
            try:
                json_str = json_match.group(1)
                order_data = json.loads(json_str)
                
                # Update Order Manager
                if st.session_state.order_manager.update_from_json(order_data):
                    st.toast("Order updated!", icon="🛒")
                
                # Remove JSON from display
                display_response = re.sub(r'```json\s*\{.*?\}\s*```', '', full_response, flags=re.DOTALL).strip()
            except Exception as e:
                print(f"JSON Parsing Error: {e}")
        
        # Typing animation
        stream = stream_text(display_response)
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": display_response})
    
    # Rerun if we updated the order to show changes in sidebar immediately
    if json_match:
        time.sleep(1) # Visual pause to let user see "Order updated" toast
        st.rerun()
    elif not json_match:
         # Standard rerun to save state? actually st.chat_input usually mandates rerun on valid input anyway, 
         # but explicit rerun ensures message history is saved before next interaction if needed.
         # Actually, st.rerun() here is safe.
         pass

# 3. VISUAL MENU GRID
st.markdown('<div class="menu-grid-header">Featured Menu</div>', unsafe_allow_html=True)

menu_items = [
    ("Dancing Fajita", "Spicy chicken fajita, onions, peppers", "Rs. 1299", PIZZA_IMG),
    ("Tarzan Tikka", "Traditional tikka flavors, spicy & rich", "Rs. 1299", PIZZA_IMG),
    ("Chicago Bold", "Deep dish style, overloaded with meat", "Rs. 1399", HERO_IMG_1),
    ("Crazy Deal 1", "2 Small Pizzas + Drinks", "Rs. 789", HERO_IMG_2),
    ("All Cheese", "Mozzarella, Cheddar, Parmesan blend", "Rs. 1199", PIZZA_IMG),
    ("Mughlai Beast", "Creamy mughlai sauce with chicken", "Rs. 1299", HERO_IMG_1),
    ("Garlic Bread", "Fresh baked with herb butter", "Rs. 399", PIZZA_IMG),
    ("Lava Cake", "Molten chocolate center dessert", "Rs. 499", HERO_IMG_2),
    ("Lunch Deal", "Pizza slice + Drink (12pm-4pm)", "Rs. 649", PIZZA_IMG),
    ("Family Feast", "2 Large Pizzas + Sides + Drinks", "Rs. 3499", HERO_IMG_2),
    ("Pepperoni", "Classic beef pepperoni & cheese", "Rs. 1249", PIZZA_IMG),
    ("BBQ Wings", "Smoky BBQ glazed wings (6 pcs)", "Rs. 599", HERO_IMG_1),
]

cols = st.columns(3)
for i, (title, desc, price, img) in enumerate(menu_items):
    with cols[i % 3]:
        with st.container():
            # Card HTML
            img_b64 = get_base64_of_bin_file(img) if os.path.exists(img) else ""
            st.markdown(f"""
                <div class="menu-card">
                    <img src="data:image/png;base64,{img_b64}" class="menu-img">
                    <div class="menu-content">
                        <div class="menu-title">{title}</div>
                        <div class="menu-desc">{desc}</div>
                        <div class="menu-price">{price}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Add {title}", key=f"add_{i}", use_container_width=True):
                 st.session_state.messages.append({"role": "user", "content": f"I want {title}"})
                 st.rerun()

