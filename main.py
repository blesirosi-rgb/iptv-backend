import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.device import router as device_router
from app.api.playlists import router as playlists_router

# ─── App ────────────────────────────────────────────────────
app = FastAPI(title="IPTV Blesio Unified Backend", version="2.0.0")

# ─── CORS ───────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ─────────────────────────────────────────────────
app.include_router(device_router, prefix="/api/device", tags=["device"])
app.include_router(playlists_router, prefix="/api/playlists", tags=["playlists"])

# ─── Root ───────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Online", "message": "Unified IPTV Backend is Live!"}