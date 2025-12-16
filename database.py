import sqlite3

DB_NAME = "data/weather.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            timestamp TEXT,
            temperature REAL,
            humidity REAL
        )
    """)
    conn.commit()
    conn.close()
