import sqlite3
import os

# Absolute path to your database
db_path = "E:/DATA ANALYST LEARNING/Advanced DE projects/Real-Time Orders with Slowly Changing Dimension/database/orders.db"

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Example: fetch all customers
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
