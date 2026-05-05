# import pandas as pd
# from utils.gemini import ask_gemini

# users = pd.read_csv("data/users.csv")
# products = pd.read_csv("data/products.csv")
# orders = pd.read_csv("data/orders.csv")

# def get_user_context(user_id: int):
#     row = users[users["user_id"] == user_id]
#     if row.empty:
#         return "User not found"
#     return row.to_dict(orient="records")[0]

# def search_products(query: str):
#     return ask_gemini(f"Recommend Pakistani clothing products for: {query}")

# def handle_support(issue: str):
#     return ask_gemini(f"Resolve customer complaint professionally: {issue}")

# def get_order_status(user_id: int):
#     row = orders[orders["user_id"] == user_id]
#     if row.empty:
#         return "No orders found"
#     return row.head(3).to_dict(orient="records")






import pandas as pd
from pathlib import Path
from utils.gemini import ask_gemini

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ==================================================
# LOAD CSV FILES
# ==================================================

users = pd.read_csv(DATA_DIR / "users.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")


# ==================================================
# USERS
# ==================================================

def get_user_context(user_id: int):
    row = users[users["user_id"] == user_id]

    if row.empty:
        return "User not found"

    return row.iloc[0].to_dict()


def get_all_users(limit: int = 10):
    return users.head(limit).to_dict(orient="records")


# ==================================================
# PRODUCTS
# ==================================================

async def search_products(query: str):
    prompt = f"""
You are Pakistani eCommerce clothing assistant.

Recommend products based on:
{query}

Use Pakistani brands like:
Khaadi, Gul Ahmed, J., Bonanza, Ideas, Outfitters, Breakout, Levis
"""
    return await ask_gemini(prompt)


def get_all_products(limit: int = 20):
    return products.head(limit).to_dict(orient="records")


def get_product_by_brand(brand: str):
    row = products[
        products["brand"].str.lower() == brand.lower()
    ]

    return row.head(20).to_dict(orient="records")


# ==================================================
# SUPPORT
# ==================================================

async def handle_support(issue: str):
    prompt = f"""
Solve this customer complaint professionally:

{issue}

Give apology + solution + next step.
"""
    return await ask_gemini(prompt)


# ==================================================
# ORDERS
# ==================================================

def get_order_status(user_id: int):
    row = orders[orders["user_id"] == user_id]

    if row.empty:
        return "No orders found"

    return row.head(10).to_dict(orient="records")


def get_order_by_id(order_id: int):
    row = orders[orders["order_id"] == order_id]

    if row.empty:
        return "Order not found"

    return row.iloc[0].to_dict()


def update_order_status(order_id: int, new_status: str):
    global orders

    idx = orders.index[orders["order_id"] == order_id]

    if len(idx) == 0:
        return "Order not found"

    orders.loc[idx, "status"] = new_status

    orders.to_csv(DATA_DIR / "orders.csv", index=False)

    return {
        "message": "Order updated successfully",
        "order_id": order_id,
        "new_status": new_status
    }