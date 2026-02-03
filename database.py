import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Render e jep URL-në e databazës përmes kësaj variable mjedisi
DATABASE_URL = os.environ.get("DATABASE_URL")

# ─── Connection ─────────────────────────────────────────────
def get_db():
    # Lidhja me PostgreSQL në Render
    # sslmode='require' është i domosdoshëm për Render
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# ─── Init DB ────────────────────────────────────────────────
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: devices
    # Kujdes: PostgreSQL përdor SERIAL për ID-të automatike
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id SERIAL PRIMARY KEY,
            mac_address TEXT UNIQUE NOT NULL,
            device_key TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            expiry_date TEXT DEFAULT NULL
        )
    """)

    # Table: playlists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id SERIAL PRIMARY KEY,
            mac_address TEXT NOT NULL,
            playlist_name TEXT NOT NULL,
            playlist_type TEXT NOT NULL,
            playlist_url TEXT NOT NULL,
            username TEXT DEFAULT NULL,
            password TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Databaza PostgreSQL u inicializua me sukses!")