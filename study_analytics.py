import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        details TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def log_activity(event_type, details=""):
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO activity (event_type, details, timestamp) VALUES (?, ?, ?)",
        (event_type, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()