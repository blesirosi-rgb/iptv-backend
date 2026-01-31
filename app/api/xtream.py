from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# --- Model (body-i i request-it) ---
class XtreamLogin(BaseModel):
    host: str
    username: str
    password: str

# --- GET / (test i filuar, mbajtje) ---
@router.get("/")
async def get_xtream():
    return {"message": "Xtream endpoint is working"}

# --- POST /login (frontend dërgon ketu) ---
@router.post("/login")
async def xtream_login(data: XtreamLogin):
    host = data.host.strip().rstrip("/")
    username = data.username.strip()
    password = data.password.strip()

    # Validim basics
    if not host or not username or not password:
        raise HTTPException(status_code=400, detail="Te gjitha fushat jane te detyroshem!")

    if not host.startswith("http"):
        raise HTTPException(status_code=400, detail="Host duhet te filloje me http:// ose https://")

    # TODO: Ketu vendos logiken tuaj
    # p.sh. lidhje te Xtream API: GET {host}/get.php?username={user}&password={pass}&type=get_info
    # Tani po kthim sukses si test

    return {
        "status": "success",
        "message": "Xtream login i suksesshme",
        "host": host,
        "username": username
    }