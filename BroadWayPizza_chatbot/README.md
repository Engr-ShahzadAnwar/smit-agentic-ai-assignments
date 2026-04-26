# 🍕 Broadway Pizza Chatbot - Paulo

Welcome to the **Broadway Pizza Chatbot** featuring **Paulo, the Friendly Pizza Waiter**! This is an AI-powered chatbot that helps customers order delicious pizzas and other menu items from Broadway Pizza Pakistan.

## ✨ Features

- 🤖 **Paulo's Warm Personality** - Friendly, conversational AI waiter
- 📋 **Complete Menu** - All pizzas, deals, appetizers, pastas, desserts, and drinks
- 🛒 **Order Management** - Create, modify, and cancel orders
- 💰 **Real-time Pricing** - Accurate prices with automatic total calculation
- 🎯 **Smart Recommendations** - Paulo suggests popular items and deals
- ✅ **Order Confirmation** - Review before finalizing
- 🎨 **Modern UI** - Beautiful Broadway Pizza-themed interface
- 📱 **Responsive Design** - Works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Run the chatbot**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 How to Use

### Ordering Pizza

Simply chat with Paulo naturally:

- "I want a large Dancing Fajita pizza"
- "Show me your deals"
- "What's popular?"
- "Add garlic bread to my order"

### Paulo's Capabilities

Paulo can help you with:

✅ **Menu Information** - Ask about any item, prices, or ingredients  
✅ **Recommendations** - Get suggestions based on popularity  
✅ **Order Taking** - Paulo asks clarifying questions (size, quantity, crust)  
✅ **Order Modification** - Add or remove items  
✅ **Deals & Offers** - Learn about current promotions  
✅ **Delivery Info** - Hours, delivery fee, minimum order  

### Quick Action Buttons

- **📋 View Full Menu** - See all available items
- **🎉 Show Me Deals** - Current promotions and offers
- **⭐ Popular Items** - Best-selling pizzas and items

## 🍕 Menu Highlights

### Gourmet Pizzas
- Chicago Bold Fold
- Dancing Fajita
- Tarzan Tikka
- Mughlai Beast
- All Cheese
- All Veggie
- MegaBite Surprise
- Phantom

**Sizes:** Small (Rs. 449) | Medium (Rs. 899) | Large (Rs. 1299) | X-Large (Rs. 1699)

### Popular Deals
- **Crazy Value Deal 1:** 2 Small Pizzas - Rs. 789
- **Crazy Value Deal 2:** 2 Medium Pizzas - Rs. 1998
- **Crazy Value Deal 3:** 2 Large Pizzas - Rs. 2798
- **Lunch Deals:** Available 10 AM - 4 PM
- **Midnight Madness:** 12 AM - 4 AM

### Appetizers & Sides
- Chicken Mega Bites (Rs. 599)
- Garlic Bread (Rs. 399)
- Mozzarella Breads (Rs. 499)
- Potato Wedges (Rs. 499)
- Starter Box (Rs. 799)

### Pastas & Desserts
- BBQ Ranch Pasta (Rs. 599)
- Spicy Garlic Ranch Pasta (Rs. 599)
- Chocolate Lava Cake (Rs. 399)

## 🛠️ Project Structure

```
BroadWayPizza_chatbot/
├── app.py                      # Main Streamlit application
├── chatbot_engine.py           # Paulo's AI brain (Gemini integration)
├── order_manager.py            # Order management system
├── broadway_menu.json          # Complete menu knowledge base
├── paulo_system_prompt.txt     # Paulo's personality & rules
├── CHATBOT_RULES.md            # Detailed system prompt rules & testing guide
├── styles.css                  # Custom UI styling
├── assets/                     # Images and static assets
├── test_order_flow.py          # Automated test suite
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🎨 Technology Stack

- **Frontend:** Streamlit with custom CSS
- **AI Engine:** Google Gemini 1.5 Flash
- **Backend:** Python 3.8+
- **Data:** JSON-based knowledge base

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Customization

- **Menu:** Edit `broadway_menu.json` to update items/prices
- **Personality:** Modify `paulo_system_prompt.txt` to adjust Paulo's behavior
- **Styling:** Update `styles.css` for UI changes

## 💡 Tips for Best Experience

1. **Be specific:** "I want a large Dancing Fajita with stuffed crust"
2. **Ask questions:** Paulo loves to help! "What's your most popular pizza?"
3. **Use deals:** Ask about current promotions to save money
4. **Review order:** Check the sidebar before confirming
5. **Natural language:** Chat like you're talking to a real waiter

## 🐛 Troubleshooting

### "Error initializing chatbot"
- Make sure you've created a `.env` file with your `GEMINI_API_KEY`
- Verify your API key is valid

### "Module not found"
- Run `pip install -r requirements.txt`

### Chat not responding
- Check your internet connection
- Verify API key is correct
- Check Gemini API quota/limits

## 📞 Contact Information

**Broadway Pizza Pakistan**  
📱 Phone: 111-339-339  
🕐 Hours: 10:00 AM - 2:00 AM  
🚚 Delivery Fee: Rs. 150  
📦 Minimum Order: Rs. 500

## 📝 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Broadway Pizza Pakistan for the delicious menu
- Google Gemini AI for powering Paulo's intelligence
- Streamlit for the amazing framework

---

**Enjoy your pizza! 🍕**

*Made with ❤️ by Paulo, your friendly AI waiter*
