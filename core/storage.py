import json
import sqlite3
from pathlib import Path


def get_connection(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
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
        CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_ip TEXT NOT NULL,
        action TEXT NOT NULL,
        down INTEGER,
        up INTEGER,
        created_at TEXT
        )
    """)
    conn.commit()


def add_device(conn, ip, mac, hostname):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO devices (ip, mac, hostname) VALUES (?, ?, ?)",
            (ip, mac, hostname),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def list_devices(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, ip, mac, hostname, status FROM devices")
    rows = cur.fetchall()
    return rows


def export_rules(conn, path):
    cur = conn.cursor()
    cur.execute("SELECT id, device_ip, action, down, up, created_at FROM rules")
    rows = cur.fetchall()
    data = [dict(row) for row in rows]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return len(data)
