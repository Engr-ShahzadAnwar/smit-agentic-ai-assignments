import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from agent import CryptoAgent
from kb_manager import KBManager
import plotly.graph_objects as go
import random

# Page configuration
st.set_page_config(
    page_title="Team 6 Crypto Markets Overview",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = CryptoAgent()
if 'kb_manager' not in st.session_state:
    st.session_state.kb_manager = KBManager()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()
if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Overview'

# Custom CSS for modern Binance-like styling
def load_custom_css():
    theme = st.session_state.theme
    
    if theme == 'dark':
        bg_color = "#0B0E11"
        card_bg = "#1E2329"
        text_color = "#EAECEF"
        secondary_text = "#848E9C"
        border_color = "#2B3139"
        hover_bg = "#2B3139"
        hover_text = "#FFFFFF"
        button_text = "#1E2329"
        button_hover_bg = "#D9A00B"
        button_hover_text = "#000000"
        positive_color = "#0ECB81"
        negative_color = "#F6465D"
        accent_color = "#F0B90B"
    else:
        bg_color = "#FAFAFA"
        card_bg = "#FFFFFF"
        text_color = "#1E2329"
        secondary_text = "#707A8A"
        border_color = "#E6E8EA"
        hover_bg = "#F5F5F5"
        hover_text = "#000000"
        button_text = "#FFFFFF"
        button_hover_bg = "#D9A00B"
        button_hover_text = "#FFFFFF"
        positive_color = "#0ECB81"
        negative_color = "#F6465D"
        accent_color = "#F0B90B"
    
    css = f"""
    <style>
        /* Main container */
        .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* Global text color */
        body, p, span, div, label, input, textarea, select {{
            color: {text_color} !important;
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Streamlit elements */
        .stMarkdown, .stText {{
            color: {text_color} !important;
        }}
        
        /* Cards */
        .crypto-card {{
            background: {card_bg};
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            color: {text_color} !important;
        }}
        
        .crypto-card:hover {{
            background: {hover_bg};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            color: {hover_text} !important;
        }}
        
        /* Ticker */
        .ticker-item {{
            background: {card_bg};
            border-radius: 6px;
            padding: 12px 16px;
            margin: 0 8px;
            border: 1px solid {border_color};
            display: inline-block;
            min-width: 180px;
            color: {text_color} !important;
        }}
        
        /* Price changes */
        .positive {{
            color: {positive_color} !important;
            font-weight: 600;
        }}
        
        .negative {{
            color: {negative_color} !important;
            font-weight: 600;
        }}
        
        /* Buttons - CRITICAL FIX */
        .stButton>button {{
            background-color: {accent_color} !important;
            color: {button_text} !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton>button:hover {{
            background-color: {button_hover_bg} !important;
            color: {button_hover_text} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }}
        
        .stButton>button:active {{
            background-color: {button_hover_bg} !important;
            color: {button_hover_text} !important;
            transform: translateY(0px) !important;
        }}
        
        .stButton>button:focus {{
            background-color: {accent_color} !important;
            color: {button_text} !important;
            outline: 2px solid {accent_color} !important;
            outline-offset: 2px !important;
        }}
        
        /* Table styling - CRITICAL FIX */
        .dataframe {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        .dataframe th {{
            background-color: {hover_bg} !important;
            color: {text_color} !important;
            font-weight: 600 !important;
            border-bottom: 2px solid {border_color} !important;
        }}
        
        .dataframe td {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-bottom: 1px solid {border_color} !important;
        }}
        
        .dataframe tr:hover {{
            background-color: {hover_bg} !important;
        }}
        
        .dataframe tr:hover td {{
            color: {hover_text} !important;
        }}
        
        /* Input fields */
        .stTextInput>div>div>input {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: {accent_color} !important;
            color: {text_color} !important;
        }}
        
        .stTextInput>div>div>input::placeholder {{
            color: {secondary_text} !important;
        }}
        
        /* Select boxes */
        .stSelectbox>div>div>div {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        /* Status badges */
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .badge-fresh {{
            background: rgba(14, 203, 129, 0.2);
            color: {positive_color} !important;
        }}
        
        .badge-stale {{
            background: rgba(246, 70, 93, 0.2);
            color: {negative_color} !important;
        }}
        
        .badge-kb {{
            background: rgba(132, 142, 156, 0.2);
            color: #848E9C !important;
        }}
        
        .badge-api {{
            background: rgba(59, 130, 246, 0.2);
            color: #3B82F6!important;
        }}
        
        /* Chat messages - CRITICAL FIX */
        .chat-message {{
            background: {card_bg} !important;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            border-left: 3px solid {accent_color};
            color: {text_color} !important;
        }}
        
        .chat-message * {{
            color: {text_color} !important;
        }}
        
        /* Detail panel */
        .detail-panel {{
            background: {card_bg};
            border-radius: 8px;
            padding: 20px;
            border: 1px solid {border_color};
            height: 100%;
            color: {text_color} !important;
        }}
        
        /* Coin icon placeholder */
        .coin-icon {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, {accent_color}, #FCD535);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: {button_text};
            margin-right: 8px;
        }}
        
        /* Metrics */
        .stMetric {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        .stMetric label {{
            color: {secondary_text} !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            color: {text_color} !important;
        }}
        
        /* Divider */
        hr {{
            border-color: {border_color} !important;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {bg_color};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {hover_bg};
        }}
        
        /* Info/Warning/Error boxes */
        .stAlert {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        /* Selectbox Dropdown Fix */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="popover"] ul {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
        }}
        
        div[data-baseweb="popover"] li {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background-color: {hover_bg} !important;
            color: {hover_text} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Generate mock price chart data
def generate_price_chart(base_price, coin_name):
    hours = 24
    timestamps = pd.date_range(end=datetime.now(), periods=hours, freq='H')
    
    # Generate realistic price movements
    prices = [base_price]
    for _ in range(hours - 1):
        change = random.uniform(-0.03, 0.03)  # ±3% change
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    fig = go.Figure()
    
    # Determine if overall trend is positive or negative
    is_positive = prices[-1] >= prices[0]
    line_color = '#0ECB81' if is_positive else '#F6465D'
    fill_color = 'rgba(14, 203, 129, 0.1)' if is_positive else 'rgba(246, 70, 93, 0.1)'
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=prices,
        mode='lines',
        name=coin_name,
        line=dict(color=line_color, width=2),
        fill='tozeroy',
        fillcolor=fill_color
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

# Get all coins from KB
def get_all_coins():
    kb_data = st.session_state.kb_manager.data.get('coins', {})
    coins_list = []
    
    for coin_key, coin_data in kb_data.items():
        # Calculate freshness
        last_updated_str = coin_data.get('last_updated', '')
        is_fresh = False
        staleness_minutes = None
        
        if last_updated_str:
            try:
                last_updated = datetime.fromisoformat(last_updated_str)
                time_diff = datetime.now() - last_updated
                staleness_minutes = time_diff.total_seconds() / 60
                is_fresh = staleness_minutes < 5
            except:
                pass
        
        # Calculate 24h change (mock for now)
        change_24h = random.uniform(-15, 15)
        volume_24h = coin_data.get('price', 0) * random.uniform(1000000, 10000000)
        
        coins_list.append({
            'key': coin_key,
            'name': coin_data.get('name', coin_key.title()),
            'symbol': coin_data.get('symbol', ''),
            'price': coin_data.get('price', 0),
            'change_24h': change_24h,
            'volume_24h': volume_24h,
            'market_cap': coin_data.get('market_cap', 0),
            'launch_year': coin_data.get('launch_year', 'N/A'),
            'consensus': coin_data.get('consensus_mechanism', 'N/A'),
            'chain_type': coin_data.get('chain_type', 'N/A'),
            'is_fresh': is_fresh,
            'staleness_minutes': staleness_minutes,
            'last_updated': last_updated_str
        })
    
    return coins_list

# Header Section
def render_header():
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("# 💎 Crypto Markets Overview")
        st.markdown("*Real-time prices and market stats*")
    
    with col2:
        # Theme toggle
        if st.button("🌓 Toggle Theme", width="stretch"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    with col3:
        st.markdown(f"**{datetime.now().strftime('%H:%M:%S')}**")
    
    # Navigation tabs
    st.markdown("---")
    tabs = ['Overview', 'Favorites', 'Spot', 'Futures', 'Help']
    cols = st.columns(len(tabs))
    
    for idx, tab in enumerate(tabs):
        with cols[idx]:
            if st.button(tab, key=f"tab_{tab}", width="stretch"):
                st.session_state.active_tab = tab
                st.rerun()

# Top Ticker Bar
def render_ticker_bar():
    st.markdown("### 📊 Top Movers")
    
    coins = get_all_coins()
    if not coins:
        st.info("No coins available in the knowledge base.")
        return
        
    top_coins = sorted(coins, key=lambda x: abs(x['change_24h']), reverse=True)[:5]
    
    # Use columns instead of raw HTML
    cols = st.columns(len(top_coins))
    
    for idx, coin in enumerate(top_coins):
        with cols[idx]:
            change_symbol = '▲' if coin['change_24h'] >= 0 else '▼'
            change_class = 'positive' if coin['change_24h'] >= 0 else 'negative'
            
            st.markdown(f"**{coin['symbol']}**")
            st.markdown(f"${coin['price']:,.2f}")
            st.markdown(f"<span class='{change_class}'>{change_symbol} {abs(coin['change_24h']):.2f}%</span>", 
                       unsafe_allow_html=True)

# Filters Section
def render_filters():
    st.markdown("### 🔍 Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        category = st.selectbox(
            "Category",
            ["All", "Favorites", "Spot", "Futures"],
            key="filter_category"
        )
    
    with col2:
        consensus_filter = st.selectbox(
            "Consensus",
            ["All", "Proof of Work", "Proof of Stake", "Proof of History", "Federated Consensus"],
            key="filter_consensus"
        )
    
    with col3:
        chain_filter = st.selectbox(
            "Chain Type",
            ["All", "Blockchain", "DAG", "Other"],
            key="filter_chain"
        )
    
    with col4:
        search_query = st.text_input("🔎 Search coin", placeholder="BTC, ETH, SOL...", key="search_input")
    
    return {
        'category': category,
        'consensus': consensus_filter,
        'chain': chain_filter,
        'search': search_query
    }

# Market Table
def render_market_table(filters):
    st.markdown("### 📈 Markets")
    
    coins = get_all_coins()
    
    if not coins:
        st.info("No coins available in the knowledge base.")
        return
    
    # Apply filters
    if filters['category'] == 'Favorites':
        coins = [c for c in coins if c['key'] in st.session_state.favorites]
    
    if filters['consensus'] != 'All':
        coins = [c for c in coins if c['consensus'] == filters['consensus']]
    
    if filters['chain'] != 'All':
        coins = [c for c in coins if c['chain_type'] == filters['chain']]
    
    if filters['search']:
        search_lower = filters['search'].lower()
        coins = [c for c in coins if 
                search_lower in c['symbol'].lower() or 
                search_lower in c['name'].lower()]
    
    if not coins:
        st.info("No coins match your filters.")
        return
    
    # Display table with click handling
    for idx, coin in enumerate(coins):
        col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 2, 1.5, 1.5, 1.5, 1.5, 1])
        
        with col1:
            # Favorite star
            is_fav = coin['key'] in st.session_state.favorites
            if st.button("⭐" if is_fav else "☆", key=f"fav_{coin['key']}_{idx}"):
                if is_fav:
                    st.session_state.favorites.remove(coin['key'])
                else:
                    st.session_state.favorites.add(coin['key'])
                st.rerun()
        
        with col2:
            st.markdown(f"**{coin['symbol']}** {coin['name']}")
        
        with col3:
            st.markdown(f"**${coin['price']:,.2f}**")
        
        with col4:
            change_class = 'positive' if coin['change_24h'] >= 0 else 'negative'
            st.markdown(f"<span class='{change_class}'>{coin['change_24h']:+.2f}%</span>", 
                       unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"${coin['volume_24h']:,.0f}")
        
        with col6:
            st.markdown(f"${coin['market_cap']:,.0f}")
        
        with col7:
            if st.button("📊", key=f"view_{coin['key']}_{idx}"):
                st.session_state.selected_coin = coin['key']
                st.rerun()
        
        st.divider()

# Detail Panel
def render_detail_panel():
    if not st.session_state.selected_coin:
        st.info("👈 Select a coin from the table to view details")
        return
    
    coin_key = st.session_state.selected_coin
    coin_data, is_fresh = st.session_state.kb_manager.get_coin_data(coin_key)
    
    if not coin_data:
        st.error("Coin data not found")
        return
    
    st.markdown(f"## {coin_data.get('name', coin_key.title())} ({coin_data.get('symbol', '')})")
    
    # Price and change
    price = coin_data.get('price', 0)
    change_24h = random.uniform(-15, 15)  # Mock
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Price", f"${price:,.2f}", f"{change_24h:+.2f}%")
    with col2:
        st.metric("Market Cap", f"${coin_data.get('market_cap', 0):,.0f}")
    
    # Freshness indicator
    if is_fresh:
        st.markdown('<span class="status-badge badge-fresh">🟢 Fresh Data</span>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge badge-stale">🟡 Stale Data</span>', 
                   unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Metadata
    st.markdown("### 📋 Metadata")
    st.markdown(f"**Launch Year:** {coin_data.get('launch_year', 'N/A')}")
    st.markdown(f"**Consensus:** {coin_data.get('consensus_mechanism', 'N/A')}")
    st.markdown(f"**Chain Type:** {coin_data.get('chain_type', 'N/A')}")
    st.markdown(f"**Last Updated:** {coin_data.get('last_updated', 'N/A')}")
    
    st.markdown("---")
    
    # Price chart
    st.markdown("### 📊 24h Price Chart")
    chart = generate_price_chart(price, coin_data.get('name', coin_key))
    st.plotly_chart(chart, width="stretch")
    
    # Confidence score
    confidence = 1.0 if is_fresh else 0.5
    st.markdown("### 🎯 Confidence Score")
    st.progress(confidence)
    st.markdown(f"**{confidence * 100:.0f}%** - {'Knowledge Base' if not is_fresh else 'Fresh Data'}")
    
    # Source tag
    source = "Knowledge Base" if not is_fresh else "FreeCryptoAPI"
    badge_class = "badge-kb" if not is_fresh else "badge-api"
    st.markdown(f'<span class="status-badge {badge_class}">{source}</span>', 
               unsafe_allow_html=True)

# Chat Console
def render_chat_console():
    st.markdown("### 💬 Agent Chat")
    
    # Chat input
    user_query = st.text_input("Ask about crypto...", 
                               placeholder="What is the price of Bitcoin?",
                               key="chat_input_field")
    
    if st.button("Send", width="stretch", key="chat_send_btn") and user_query:
        # Process query
        response = st.session_state.agent.process_query(user_query)
        
        # Add to history
        st.session_state.chat_history.append({
            'timestamp': datetime.now(),
            'query': user_query,
            'response': response
        })
        
        st.rerun()
    
    # Display chat history
    st.markdown("---")
    
    if not st.session_state.chat_history:
        st.info("No chat history yet. Ask a question above!")
    else:
        # Show last 5 messages
        for chat in reversed(st.session_state.chat_history[-5:]):
            st.markdown(f"""
            <div class="chat-message">
                <div style="font-size: 12px; color: #848E9C; margin-bottom: 4px;">
                    {chat['timestamp'].strftime('%H:%M:%S')}
                </div>
                <div style="font-weight: 600; margin-bottom: 8px;">
                    👤 {chat['query']}
                </div>
                <div style="margin-bottom: 8px;">
                    🤖 {chat['response'].get('answer', 'No response')}
                </div>
                <div style="font-size: 12px;">
                    <span class="status-badge badge-api">Source: {chat['response'].get('source', 'N/A')}</span>
                    <span class="status-badge badge-fresh">Confidence: {chat['response'].get('confidence', 0) * 100:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# KB Inspector
def render_kb_inspector():
    st.markdown("### 🗄️ Knowledge Base Inspector")
    
    kb_data = st.session_state.kb_manager.data.get('coins', {})
    
    if not kb_data:
        st.info("Knowledge base is empty")
        return
    
    # Create table
    inspector_data = []
    for coin_key, coin_info in kb_data.items():
        inspector_data.append({
            'Coin': coin_info.get('name', coin_key),
            'Symbol': coin_info.get('symbol', ''),
            'Price': f"${coin_info.get('price', 0):,.2f}",
            'Last Updated': coin_info.get('last_updated', 'N/A'),
            'Launch Year': coin_info.get('launch_year', 'N/A'),
            'Consensus': coin_info.get('consensus_mechanism', 'N/A')
        })
    
    df = pd.DataFrame(inspector_data)
    st.dataframe(df, width="stretch", hide_index=True)

# Status Bar
def render_status_bar():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**API Status:** 🟢 Online")
    
    with col2:
        st.markdown("**Freshness Threshold:** 5 minutes")
    
    with col3:
        last_sync = datetime.now().strftime('%H:%M:%S')
        st.markdown(f"**Last Sync:** {last_sync}")
    
    with col4:
        kb_count = len(st.session_state.kb_manager.data.get('coins', {}))
        st.markdown(f"**KB Entries:** {kb_count}")

# Main App
def main():
    load_custom_css()
    
    # Header
    render_header()
    
    # Ticker Bar
    render_ticker_bar()
    st.markdown("---")
    
    # Main content area
    if st.session_state.active_tab == 'Overview':
        # Filters
        filters = render_filters()
        
        # Main layout: Market Table + Detail Panel
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_market_table(filters)
        
        with col2:
            render_detail_panel()
        
        st.markdown("---")
        
        # Bottom section: Chat + KB Inspector
        col1, col2 = st.columns(2)
        
        with col1:
            render_chat_console()
        
        with col2:
            render_kb_inspector()
    
    elif st.session_state.active_tab == 'Favorites':
        st.markdown("### ⭐ Your Favorites")
        if not st.session_state.favorites:
            st.info("No favorites yet. Click the star icon next to any coin to add it!")
        else:
            filters = {'category': 'Favorites', 'consensus': 'All', 'chain': 'All', 'search': ''}
            
            col1, col2 = st.columns([2, 1])
            with col1:
                render_market_table(filters)
            with col2:
                render_detail_panel()
    
    elif st.session_state.active_tab == 'Help':
        st.markdown("### ❓ Help & Documentation")
        st.markdown("""
        **How to use this app:**
        
        1. **Browse Markets**: View all available cryptocurrencies in the main table
        2. **Filter & Search**: Use the filters to narrow down coins by consensus, chain type, or search
        3. **View Details**: Click the 📊 button to see detailed information about a coin
        4. **Add Favorites**: Click the ⭐ icon to add coins to your favorites list
        5. **Chat with Agent**: Ask questions about cryptocurrencies in the chat console
        6. **Inspect KB**: View the raw knowledge base data in the KB Inspector
        
        **Data Sources:**
        - 🟢 Fresh: Data updated within the last 5 minutes
        - 🟡 Stale: Data older than 5 minutes
        - Knowledge Base: Cached local data
        - FreeCryptoAPI: Live API data
        
        **Color Coding:**
        - Green: Positive price change
        - Red: Negative price change
        - Blue: API fetched data
        - Grey: Cached KB data
        """)
    
    else:
        st.info(f"The {st.session_state.active_tab} section is coming soon!")
    
    # Status Bar
    st.markdown("---")
    render_status_bar()

if __name__ == "__main__":
    main()
