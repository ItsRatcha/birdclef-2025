import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("train.csv")

# Create SQLite DB
conn = sqlite3.connect("train.db")

# Write to DB (table name: 'train_data')
df.to_sql("train_data", conn, if_exists="replace", index=False)

conn.close()
