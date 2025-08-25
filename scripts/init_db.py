import sqlite3

# Connect to (or create) database file
conn = sqlite3.connect("database/orders.db")
cursor = conn.cursor()

# Create Customers table (SCD2 style)
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER,
    name TEXT,
    email TEXT,
    start_date TEXT,
    end_date TEXT,
    is_current INTEGER
)
""")

# Create Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    order_date TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized with customers and orders tables!")
