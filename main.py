import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Sigurohemi që Python të gjejë dosjen 'app' për importet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.device import router as device_router
from app.api.playlists import router as playlists_router

# ─── App Configuration ───
app = FastAPI(title="BlesioIPTV Unified Backend", version="2.0.0")

# ─── CORS (E rëndësishme për Netlify) ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ───
app.include_router(device_router, prefix="/api/device", tags=["device"])
app.include_router(playlists_router, prefix="/api/playlists", tags=["playlists"])

# ─── Root Endpoint ───
@app.get("/")
def root():
    return {
        "status": "Online",
        "message": "BlesioIPTV Backend is Live!",
        "version": "2.0.0"
    }

# ─── Render / Start Logic ───
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)