import sqlite3
from pathlib import Path


def get_connection(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn  = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn 


def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT UNIQUE NOT NULL,
        mac TEXT,
        hostname TEXT,
        vendor TEXT,
        first_seen TEXT,
        last_seen TEXT,
        status TEXT DEFAULT 'active'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_ip TEXT NOT NULL,
        action TEXT NOT NULL,
        down INTEGER,
        up INTEGER,
        created_at TEXT
        )
    """)
    conn.commit()