from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import get_db  # Sigurohu që ky import është i saktë sipas strukturës tënde
from psycopg2.extras import RealDictCursor

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
@router.get("/{mac_address}")
async def get_playlists(mac_address: str):
    mac = mac_address.strip().upper()
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Përdorim RealDictCursor që rezultati të vijë si JSON (fjalor)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM playlists WHERE mac_address = %s", (mac,))
        playlists = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "playlists": playlists
        }
    except Exception as e:
        if conn: conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# ─── POST /add ──────────────────────────────────────────────
@router.post("/add")
async def add_playlist(data: PlaylistAdd):
    mac = data.mac_address.strip().upper()
    name = data.playlist_name.strip()
    ptype = data.playlist_type.strip().upper()
    url = data.playlist_url.strip()
    
    if not mac or not name or not url:
        raise HTTPException(status_code=400, detail="Të gjitha fushat janë të detyrueshme!")

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO playlists (mac_address, playlist_name, playlist_type, playlist_url, username, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (mac, name, ptype, url, data.username, data.password))
        
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "success": True,
            "message": "Playlist u shtua me sukses!",
            "id": new_id
        }
    except Exception as e:
        if conn: conn.rollback(); conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# ─── PUT /{id} ──────────────────────────────────────────────
@router.put("/{id}")
async def update_playlist(id: int, data: PlaylistUpdate):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE playlists 
            SET playlist_name = %s, playlist_url = %s, username = %s, password = %s
            WHERE id = %s
        """, (data.playlist_name, data.playlist_url, data.username, data.password, id))
        
        if cursor.rowcount == 0:
            cursor.close(); conn.close()
            raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Playlist u ndryshua me sukses!"}
    except Exception as e:
        if conn: conn.rollback(); conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# ─── DELETE /{id} ───────────────────────────────────────────
@router.delete("/{id}")
async def delete_playlist(id: int):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM playlists WHERE id = %s", (id,))
        
        if cursor.rowcount == 0:
            cursor.close(); conn.close()
            raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")
            
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Playlist u fshi me sukses!"}
    except Exception as e:
        if conn: conn.rollback(); conn.close()
        raise HTTPException(status_code=500, detail=str(e))