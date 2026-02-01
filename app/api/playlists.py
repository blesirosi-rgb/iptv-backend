from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter()

# ─── Models ─────────────────────────────────────────────────
class PlaylistAdd(BaseModel):
    mac_address: str
    playlist_type: str
    playlist_url: str
    playlist_name: str
    username: Optional[str] = None
    password: Optional[str] = None

class PlaylistUpdate(BaseModel):
    playlist_url: str
    playlist_name: str
    username: Optional[str] = None
    password: Optional[str] = None

# ─── GET /{mac_address} ─────────────────────────────────────
# Ngarkim te gjitha playlists nga nje device
@router.get("/{mac_address}")
async def get_playlists(mac_address: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM playlists WHERE mac_address = ?", (mac_address.upper(),))
    rows = cursor.fetchall()
    conn.close()

    playlists = []
    for row in rows:
        playlists.append({
            "id": row["id"],
            "playlist_name": row["playlist_name"],
            "playlist_type": row["playlist_type"],
            "playlist_url": row["playlist_url"],
            "username": row["username"],
            "password": row["password"]
        })

    return {
        "success": True,
        "playlists": playlists
    }

# ─── POST /add ──────────────────────────────────────────────
# Shtim playlist te re
@router.post("/add")
async def add_playlist(data: PlaylistAdd):
    mac = data.mac_address.strip().upper()
    name = data.playlist_name.strip()
    ptype = data.playlist_type.strip().upper()
    url = data.playlist_url.strip()
    username = data.username.strip() if data.username else None
    password = data.password.strip() if data.password else None

    if not mac:
        raise HTTPException(status_code=400, detail="MAC address i detyroshem!")
    if not name:
        raise HTTPException(status_code=400, detail="Playlist name i detyroshem!")
    if not url:
        raise HTTPException(status_code=400, detail="Playlist URL i detyroshem!")
    if ptype not in ["M3U", "XTREAM", "STALKER"]:
        raise HTTPException(status_code=400, detail="Playlist type i gauar! (M3U, XTREAM, STALKER)")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO playlists (mac_address, playlist_name, playlist_type, playlist_url, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (mac, name, ptype, url, username, password))

    conn.commit()
    playlist_id = cursor.lastrowid
    conn.close()

    return {
        "success": True,
        "message": "Playlist u shtua me sukses!",
        "id": playlist_id
    }

# ─── PUT /{id} ──────────────────────────────────────────────
# Ndryshim playlist nga ID
@router.put("/{id}")
async def update_playlist(id: int, data: PlaylistUpdate):
    name = data.playlist_name.strip()
    url = data.playlist_url.strip()
    username = data.username.strip() if data.username else None
    password = data.password.strip() if data.password else None

    if not name:
        raise HTTPException(status_code=400, detail="Playlist name i detyroshem!")
    if not url:
        raise HTTPException(status_code=400, detail="Playlist URL i detyroshem!")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM playlists WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")

    cursor.execute("""
        UPDATE playlists
        SET playlist_name = ?, playlist_url = ?, username = ?, password = ?
        WHERE id = ?
    """, (name, url, username, password, id))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Playlist u ndryshuar me sukses!"
    }

# ─── DELETE /{id} ───────────────────────────────────────────
# Fshirje playlist nga ID
@router.delete("/{id}")
async def delete_playlist(id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM playlists WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")

    cursor.execute("DELETE FROM playlists WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Playlist u fshi me sukses!"
    }