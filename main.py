import sysimport os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db # ✅ Importo funksionin e krijimit te tabelave

# Sigurohemi që Python të gjejë dosjen 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.device import router as device_router
from app.api.playlists import router as playlists_router

app = FastAPI(title="BlesioIPTV Backend", version="2.0.0")

# Inicializojmë Tabelat në PostgreSQL sapo ndizet serveri
@app.on_event("startup")
async def startup_event():
    init_db() # ✅ Kjo krijon tabelat devices dhe playlists nese nuk jane

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device_router, prefix="/api/device", tags=["device"])
app.include_router(playlists_router, prefix="/api/playlists", tags=["playlists"])

@app.get("/")
def root():
    return {"status": "Online", "message": "BlesioIPTV Backend is Live!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)