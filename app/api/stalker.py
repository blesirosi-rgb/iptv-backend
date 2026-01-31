from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# --- Model (body-i i request-it) ---
class StalkerLogin(BaseModel):
    mac: str
    device_key: Optional[str] = None

# --- GET / (test i filuar, mbajtje) ---
@router.get("/")
async def get_stalker():
    return {"message": "Stalker endpoint is working"}

# --- POST /login (frontend dërgon ketu) ---
@router.post("/login")
async def stalker_login(data: StalkerLogin):
    mac = data.mac.strip()
    device_key = data.device_key

    # Validim basics
    if not mac:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="MAC Address i detyroshem!")

    # TODO: Ketu vendos logiken tuaj te aderave
    # p.sh. lidhje te Stalker Portal API te server-it tuaj
    # Tani po kthim sukses si test

    return {
        "status": "success",
        "message": "Stalker login i suksesshme",
        "mac": mac,
        "device_key": device_key
    }