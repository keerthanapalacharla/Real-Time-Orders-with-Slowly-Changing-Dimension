import os
import sqlite3
import pandas as pd
import time
import shutil

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"
DB_PATH = "database/orders.db"

def ingest_new_files():
    for file in os.listdir(RAW_FOLDER):
        if file.endswith(".csv"):
            file_path = os.path.join(RAW_FOLDER, file)
            print(f"📥 Found new file: {file}")

            # Read CSV into DataFrame
            df = pd.read_csv(file_path)

            # Connect to SQLite
            conn = sqlite3.connect(DB_PATH)

            # Append data into orders table
            df.to_sql("orders", conn, if_exists="append", index=False)

            conn.close()

            # Move file to processed
            shutil.move(file_path, os.path.join(PROCESSED_FOLDER, file))
            print(f"✅ {file} ingested and moved to processed folder")

def watch_folder():
    print("👀 Watching for new files... (Press CTRL+C to stop)")
    while True:
        ingest_new_files()
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    watch_folder()
