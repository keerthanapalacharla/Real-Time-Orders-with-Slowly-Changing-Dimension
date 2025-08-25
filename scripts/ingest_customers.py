import sqlite3
from datetime import datetime
import os

# Absolute path to database
db_path = "E:/DATA ANALYST LEARNING/Advanced DE projects/Real-Time Orders with Slowly Changing Dimension/database/orders.db"

# Ensure the database folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create customers table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT,
    name TEXT,
    email TEXT,
    start_date TEXT,
    is_current INTEGER,
    PRIMARY KEY(customer_id, start_date)
)
""")
conn.commit()

# Add expiry_date column if missing
columns = [row[1] for row in cursor.execute("PRAGMA table_info(customers)")]
if 'expiry_date' not in columns:
    cursor.execute("ALTER TABLE customers ADD COLUMN expiry_date TEXT")
    conn.commit()

def upsert_customer(customer_id, name, email):
    """
    Insert a new customer or update existing for SCD Type-2.
    """
    # 1. Check if a current record exists
    cursor.execute("""
        SELECT * FROM customers
        WHERE customer_id = ? AND is_current = 1
    """, (customer_id,))
    existing = cursor.fetchone()

    if existing:
        # 2. Check if any change in name/email
        if existing[1] != name or existing[2] != email:
            # Expire the old record
            cursor.execute("""
                UPDATE customers
                SET expiry_date = ?, is_current = 0
                WHERE customer_id = ? AND is_current = 1
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), customer_id))
            conn.commit()

            # Insert new version of the record
            cursor.execute("""
                INSERT INTO customers (customer_id, name, email, start_date, expiry_date, is_current)
                VALUES (?, ?, ?, ?, NULL, 1)
            """, (customer_id, name, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
    else:
        # No existing record, insert new
        cursor.execute("""
            INSERT INTO customers (customer_id, name, email, start_date, expiry_date, is_current)
            VALUES (?, ?, ?, ?, NULL, 1)
        """, (customer_id, name, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

# Example usage
customers = [
    ("C001", "Alice", "alice@example.com"),
    ("C002", "Bob", "bob@example.com"),
    ("C001", "Alice Smith", "alice.smith@example.com")  # Update example
]

for cust in customers:
    upsert_customer(*cust)

# Check table content
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
