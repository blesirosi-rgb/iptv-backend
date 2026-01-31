from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_xtream():
    return {"message": "Xtream endpoint is working"}