from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# ─── In-Memory Storage ──────────────────────────────────────
# Playlists ruhen ne memory — nuk nevroj database
# Format: { "MAC_ADDRESS": [ {playlist}, {playlist}, ... ] }
playlists_db = {}
next_id = 1  # Auto-increment ID

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
    playlists = playlists_db.get(mac, [])

    return {
        "success": True,
        "playlists": playlists
    }

# ─── POST /add ──────────────────────────────────────────────
@router.post("/add")
async def add_playlist(data: PlaylistAdd):
    global next_id

    mac = data.mac_address.strip().upper()
    name = data.playlist_name.strip()
    ptype = data.playlist_type.strip().upper()
    url = data.playlist_url.strip()
    username = data.username.strip() if data.username else None
    password = data.password.strip() if data.password else None

    # Validim
    if not mac:
        raise HTTPException(status_code=400, detail="MAC address i detyroshem!")
    if not name:
        raise HTTPException(status_code=400, detail="Playlist name i detyroshem!")
    if not url:
        raise HTTPException(status_code=400, detail="Playlist URL i detyroshem!")
    if ptype not in ["M3U", "XTREAM", "STALKER"]:
        raise HTTPException(status_code=400, detail="Playlist type i gauar! (M3U, XTREAM, STALKER)")

    # Kriim playlist
    playlist = {
        "id": next_id,
        "playlist_name": name,
        "playlist_type": ptype,
        "playlist_url": url,
        "username": username,
        "password": password
    }
    next_id += 1

    # Ruaj ne memory
    if mac not in playlists_db:
        playlists_db[mac] = []
    playlists_db[mac].append(playlist)

    return {
        "success": True,
        "message": "Playlist u shtua me sukses!",
        "id": playlist["id"]
    }

# ─── PUT /{id} ──────────────────────────────────────────────
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

    # Kerkim playlist nga ID te gjitha MAC-t
    for mac in playlists_db:
        for playlist in playlists_db[mac]:
            if playlist["id"] == id:
                playlist["playlist_name"] = name
                playlist["playlist_url"] = url
                playlist["username"] = username
                playlist["password"] = password
                return {
                    "success": True,
                    "message": "Playlist u ndryshuar me sukses!"
                }

    raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")

# ─── DELETE /{id} ───────────────────────────────────────────
@router.delete("/{id}")
async def delete_playlist(id: int):
    # Kerkim dhe fshim playlist nga ID
    for mac in playlists_db:
        for i, playlist in enumerate(playlists_db[mac]):
            if playlist["id"] == id:
                playlists_db[mac].pop(i)
                return {
                    "success": True,
                    "message": "Playlist u fshi me sukses!"
                }

    raise HTTPException(status_code=404, detail="Playlist nuk u gjet!")