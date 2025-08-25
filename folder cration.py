import os

# Define folders
folders = [
    "data/raw",        # Incoming CSV files (new orders)
    "data/processed",  # Processed CSVs archived here
    "scripts",         # Python scripts
    "database"         # SQLite database file stored here
]

# Create the folders if they don’t exist
for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("✅ Project folders created successfully!")
