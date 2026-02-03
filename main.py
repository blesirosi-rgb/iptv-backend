import sysimport os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Sigurohemi që Python të gjejë dosjen 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.device import router as device_router
from app.api.playlists import router as playlists_router

# ─── App ────────────────────────────────────────────────────
app = FastAPI(title="IPTV Blesio Unified Backend", version="2.0.0")

# ─── CORS (E RËNDËSISHME PËR NETLIFY) ────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lejon Web Panelin të dërgojë të dhëna
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
    return {
        "status": "Online", 
        "message": "Unified IPTV Backend is Live!",
        "version": "2.0.0"
    }

# ─── RENDER START LOGIC ─────────────────────────────────────
if __name__ == "__main__":
    # Render e cakton portën vetë, kjo linjë e gjen atë automatikisht
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)