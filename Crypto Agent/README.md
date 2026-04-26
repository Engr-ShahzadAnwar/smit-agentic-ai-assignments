# 💎 Crypto Markets Overview - Streamlit App

A modern, Binance-style crypto markets overview dashboard built with Streamlit.

## Features

### 🎨 Modern UI Components

1. **Header Section**
   - Dynamic title and subtitle
   - Dark/Light theme toggle
   - Navigation tabs: Overview | Favorites | Spot | Futures | Help
   - Real-time clock display

2. **Top Ticker Bar**
   - Shows top 5 movers by 24h change
   - Displays coin symbol, current price, and 24h % change
   - Color-coded: Green (positive) / Red (negative)
   - Horizontal scrollable layout

3. **Advanced Filters**
   - Category filter: All / Favorites / Spot / Futures
   - Consensus mechanism filter
   - Chain type filter
   - Real-time search by coin symbol or name

4. **Interactive Market Table**
   - Sortable columns: Coin | Price | 24h Change | 24h Volume | Market Cap | Source
   - Favorite toggle (⭐) for each coin
   - Click-to-view details (📊) button
   - Color-coded price changes
   - Freshness indicators (🟢 Fresh / 🟡 Stale)

5. **Detail Panel**
   - Comprehensive coin metadata
   - Launch year, consensus mechanism, chain type
   - Interactive 24h price chart (Plotly)
   - Confidence score visualization
   - Source badge (Knowledge Base / FreeCryptoAPI)
   - Freshness status indicator

6. **Agent Chat Console**
   - Interactive chat interface
   - Query the crypto agent about any coin
   - Displays:
     - User questions
     - Agent responses
     - Source attribution
     - Confidence scores
   - Chat history (last 5 messages)

7. **Knowledge Base Inspector**
   - Table view of all KB entries
   - Shows coin name, symbol, price, last updated timestamp
   - Metadata display (launch year, consensus)

8. **Status Bar**
   - API status indicator
   - Freshness threshold display
   - Last sync timestamp
   - Total KB entries count

## 🎨 Design Features

- **Modern Color Scheme**: Binance-inspired dark/light themes
- **Color Coding**:
  - 🟢 Green: Positive price changes
  - 🔴 Red: Negative price changes
  - 🔵 Blue: API-fetched data
  - ⚪ Grey: Cached KB data
- **Responsive Layout**: Adapts to different screen sizes
- **Smooth Animations**: Hover effects and transitions
- **Professional Typography**: Clean, readable fonts

## 🚀 Installation

1. **Activate Virtual Environment**:
   ```bash
   .\crypto_venv\Scripts\Activate.ps1  # Windows PowerShell
   # OR
   source crypto_venv/bin/activate     # Linux/Mac
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📱 Usage

1. **Run the Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Navigate the Interface**:
   - Browse all coins in the main table
   - Use filters to narrow down results
   - Click ⭐ to add coins to favorites
   - Click 📊 to view detailed coin information
   - Ask questions in the chat console
   - Toggle between dark/light themes

3. **Chat with the Agent**:
   - Type questions like:
     - "What is the price of Bitcoin?"
     - "Tell me about Ethereum"
     - "What is the consensus mechanism of Solana?"
   - View responses with source attribution and confidence scores

## 📊 Data Sources

- **Knowledge Base**: Local cached data (JSON file)
- **FreeCryptoAPI**: Live API data (when KB is stale)
- **Freshness Threshold**: 5 minutes

## 🔧 Configuration

### Freshness Threshold
Edit `kb_manager.py`:
```python
FRESHNESS_THRESHOLD_MINUTES = 5  # Change as needed
```

### Theme Colors
Customize colors in `streamlit_app.py` in the `load_custom_css()` function.

## 📁 Project Structure

```
Crypto Agent/
├── streamlit_app.py       # Main Streamlit application
├── agent.py               # Crypto agent logic
├── kb_manager.py          # Knowledge base management
├── api_client.py          # API client for FreeCryptoAPI
├── knowledge_base.json    # Local coin data storage
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎯 Key Features Implemented

✅ Header with theme toggle and navigation  
✅ Top ticker bar with top movers  
✅ Advanced filters (category, consensus, chain, search)  
✅ Interactive market table with favorites  
✅ Detail panel with metadata and charts  
✅ Agent chat console with history  
✅ Knowledge Base inspector  
✅ Status bar with real-time info  
✅ Dark/Light theme support  
✅ Color-coded price changes  
✅ Freshness indicators  
✅ Confidence scores  
✅ Source attribution  

## 🔥 Optional Enhancements Included

⭐ Watchlist/Favorites toggle  
📊 24h price charts (Plotly)  
📌 Staleness badges  
🎨 Modern Binance-style UI  
🌓 Theme switcher  
💬 Interactive chat interface  

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Python**: Core logic and agent

## 📝 Notes

- The app uses mock data for 24h changes and volumes (can be replaced with real API data)
- Price charts are generated with realistic random movements
- All timestamps are in local timezone
- The agent follows strict rules: no predictions, no investment advice

## 🎓 Educational Purpose

This project demonstrates:
- Building modern web UIs with Streamlit
- Implementing knowledge-first agent patterns
- Creating interactive data visualizations
- Managing local knowledge bases
- Integrating external APIs
- Designing professional dashboards

---

**Created for**: SMIT Batch 8 - AI Agentic Course  
**Assignment**: Crypto Agent with Markets Overview UI
