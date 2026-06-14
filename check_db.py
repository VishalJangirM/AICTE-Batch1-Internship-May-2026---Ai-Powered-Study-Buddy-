import sqlite3
import pandas as pd

conn = sqlite3.connect("studybuddy.db")

df = pd.read_sql_query(
    "SELECT * FROM activity",
    conn
)

print(df)

conn.close()