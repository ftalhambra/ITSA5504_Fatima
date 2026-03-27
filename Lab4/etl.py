import requests
import sqlite3

USD_TO_EUR = 0.92

# Extract
orders = requests.get("http://127.0.0.1:5000/orders").json()

# Connect to SQLite
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    item TEXT,
    price_eur REAL
)
""")

# Transform + Load
for order in orders:
    price_eur = order["price_usd"] * USD_TO_EUR
    cursor.execute(
        "INSERT INTO orders VALUES (?, ?, ?)",
        (order["order_id"], order["item"], price_eur)
    )

conn.commit()
conn.close()

print("✅ ETL completed successfully")