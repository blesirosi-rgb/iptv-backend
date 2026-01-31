from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_stalker():
    return {"message": "Stalker endpoint is working"}