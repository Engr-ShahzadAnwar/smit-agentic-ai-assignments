import pandas as pd
import random
from faker import Faker

fake = Faker("en_US")

urdu_names = [
    "Ahmed Ali","Muhammad Bilal","Usman Khan","Hassan Raza",
    "Fatima Noor","Ayesha Khan","Zainab Ali","Maryam Ahmed",
    "Ali Hamza","Saad Ahmed"
]

karachi_areas = [
    "Gulshan-e-Iqbal","North Nazimabad","Clifton",
    "Saddar","Korangi","Malir","Nazimabad",
    "PECHS","DHA","Liaquatabad"
]

brands = [
    "Khaadi","Gul Ahmed","J.","Bonanza",
    "Ideas","Outfitters","Breakout","Levis"
]

categories = [
    "Kurta","Shirt","Jeans","T-Shirt",
    "Hoodie","Jacket","Trouser"
]

# USERS
users = []

for i in range(1,1001):
    users.append({
        "user_id": i,
        "name": random.choice(urdu_names),
        "email": f"user{i}@gmail.com",
        "phone": f"03{random.randint(100000000,999999999)}",
        "city": "Karachi",
        "area": random.choice(karachi_areas),
        "orders": random.randint(0,20),
        "vip_status": random.choice(["Yes","No"])
    })

pd.DataFrame(users).drop_duplicates().to_csv("data/users.csv",index=False)

# PRODUCTS
products = []

for i in range(1,501):
    brand = random.choice(brands)
    cat = random.choice(categories)

    products.append({
        "product_id": i,
        "name": f"{brand} {cat}",
        "brand": brand,
        "category": cat,
        "price": random.randint(1500,8500),
        "stock": random.randint(5,200),
        "rating": round(random.uniform(3.5,5.0),1)
    })

pd.DataFrame(products).drop_duplicates().to_csv("data/products.csv",index=False)

# ORDERS
orders = []

for i in range(1,2001):
    orders.append({
        "order_id": i,
        "user_id": random.randint(1,1000),
        "product_id": random.randint(1,500),
        "quantity": random.randint(1,3),
        "status": random.choice(["Delivered","Pending","Cancelled"]),
        "payment": random.choice(["COD","Card","JazzCash","EasyPaisa"])
    })

pd.DataFrame(orders).drop_duplicates().to_csv("data/orders.csv",index=False)

print("✅ Data Generated")