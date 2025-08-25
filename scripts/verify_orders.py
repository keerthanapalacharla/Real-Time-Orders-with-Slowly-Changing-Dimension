import sqlite3
import pandas as pd

# Path to the SQLite DB
DB_PATH = "database/orders.db"

def verify_orders():
    # Connect to the DB
    conn = sqlite3.connect(DB_PATH)

    # Read all rows from orders table
    query = "SELECT * FROM orders"
    df = pd.read_sql_query(query, conn)

    conn.close()

    # Print results
    if df.empty:
        print("⚠️ No records found in orders table.")
    else:
        print("✅ Orders table data:")
        print(df)

if __name__ == "__main__":
    verify_orders()
