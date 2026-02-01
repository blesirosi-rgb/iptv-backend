import sqlite3
import os

DB_PATH = "iptv.db"

# ─── Connection ─────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─── Init DB ────────────────────────────────────────────────
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: devices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_address TEXT UNIQUE NOT NULL,
            device_key TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            expiry_date TEXT DEFAULT NULL
        )
    """)

    # Table: playlists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_address TEXT NOT NULL,
            playlist_name TEXT NOT NULL,
            playlist_type TEXT NOT NULL,
            playlist_url TEXT NOT NULL,
            username TEXT DEFAULT NULL,
            password TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()