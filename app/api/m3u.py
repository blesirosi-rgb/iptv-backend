from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# --- Model (body-i i request-it) ---
class M3UAdd(BaseModel):
    url: str

# --- GET / (test i filuar, mbajtje) ---
@router.get("/")
async def get_m3u():
    return {"message": "M3U endpoint is working"}

# --- POST /add (frontend dërgon ketu) ---
@router.post("/add")
async def add_m3u(data: M3UAdd):
    url = data.url.strip()

    # Validim basics
    if not url:
        raise HTTPException(status_code=400, detail="M3U URL i detyroshem!")

    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL duhet te filloje me http:// ose https://")

    # TODO: Ketu vendos logiken tuaj
    # p.sh. download playlist, parse channels, ruaj ne database
    # Tani po kthim sukses si test

    return {
        "status": "success",
        "message": "M3U Playlist shtuara me sukses",
        "url": url
    }