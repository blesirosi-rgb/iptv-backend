import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.api.m3u import router as m3u_router
    from app.api.xtream import router as xtream_router
    from app.api.stalker import router as stalker_router
except ImportError as e:
    print(f"GABIM NE IMPORTIM: {e}")
    raise e

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

app = FastAPI(title="IPTV Blesio Unified Backend", version="1.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════
# UNIFIED MODELS (M3U, Xtream, Stalker)
# ════════════════════════════════════════════════════════════
class DeviceVerifyRequest(BaseModel):
    mac_address: str
    device_key: str

class DeviceInfo(BaseModel):
    mac_address: str
    status: str = "active"
    expiry_date: Optional[str] = "Unlimited"

class RemotePlaylist(BaseModel):
    id: int
    name: str
    url: str
    type: str  # "m3u", "xtream", ose "stalker"
    username: Optional[str] = None
    password: Optional[str] = None
    mac_address: Optional[str] = None # Specifike per Stalker

class BlesioResponse(BaseModel):
    success: bool
    message: str
    device: Optional[DeviceInfo] = None
    playlists: List[RemotePlaylist] = []

# ════════════════════════════════════════════════════════════
# UNIVERSAL VERIFICATION ENDPOINT
# ════════════════════════════════════════════════════════════

@app.post("/api/device/verify", response_model=BlesioResponse)
async def verify_device(request: DeviceVerifyRequest):
    # Këtu po krijojmë një listë shembull që përmban të 3 llojet
    # Në të ardhmen, këto do të vijnë nga Database jote
    combined_playlists = [
        RemotePlaylist(
            id=1, 
            name="Lista Ime M3U", 
            url="http://serveri-yt.com/playlist.m3u", 
            type="m3u"
        ),
        RemotePlaylist(
            id=2, 
            name="Linja Xtream", 
            url="http://xtream-dns.com:8080", 
            type="xtream",
            username="user123",
            password="pass123"
        ),
        RemotePlaylist(
            id=3, 
            name="Portal Stalker", 
            url="http://stalker-portal.com/c/", 
            type="stalker",
            mac_address=request.mac_address # Përdor MAC-un e pajisjes
        )
    ]

    return BlesioResponse(
        success=True,
        message="Pajisja u verifikua. Të gjitha listat u ngarkuan.",
        device=DeviceInfo(mac_address=request.mac_address),
        playlists=combined_playlists
    )

# Regjistrimi i rrugëve ekzistuese
app.include_router(m3u_router, prefix="/api/m3u", tags=["m3u"])
app.include_router(stalker_router, prefix="/api/stalker", tags=["stalker"])
app.include_router(xtream_router, prefix="/api/xtream", tags=["xtream"])

@app.get("/")
def root():
    return {"status": "Online", "message": "Unified IPTV Backend is Live!"}