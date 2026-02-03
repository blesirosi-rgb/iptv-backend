import psycopg2
from psycopg2.extras import RealDictCursor
import os

# 🔐 SIGURIA: Nuk e shkruajmë linkun këtu. 
# Kodi e kërkon atë automatikisht te "Environment Variables" të Render.
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        # Nëse harron ta vendosësh në Render, ky mesazh do të të njoftojë
        print("❌ GABIM: DATABASE_URL nuk u gjet! Konfiguroje në Render.")
        return None
    
    # Lidhja me PostgreSQL në Render
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def init_db():
    conn = get_db()
    if conn is None: return
    
    cursor = conn.cursor()

    # Tabela e pajisjeve
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id SERIAL PRIMARY KEY,
            mac_address TEXT UNIQUE NOT NULL,
            device_key TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            expiry_date TEXT DEFAULT NULL
        )
    """)

    # Tabela e playlistave
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
    print("✅ Databaza PostgreSQL u inicializua në mënyrë të sigurt!")