from fastapi import APIRouter

# Ky është emri që kërkon main.py
router = APIRouter()

@router.get("/")
async def get_m3u():
    return {"message": "M3U endpoint is working"}