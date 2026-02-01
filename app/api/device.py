from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ─── Model ──────────────────────────────────────────────────
class DeviceVerifyRequest(BaseModel):
    mac_address: str
    device_key: str

# ─── POST /verify ───────────────────────────────────────────
# Open login — pranoj cdo MAC + device key
# Keshtu login punoi nga telefoni i cili ka MAC real dhe key random
@router.post("/verify")
async def verify_device(request: DeviceVerifyRequest):
    mac = request.mac_address.strip().upper()
    key = request.device_key.strip()

    if not mac or not key:
        raise HTTPException(status_code=400, detail="MAC address dhe device key janë detyrimshme!")

    return {
        "success": True,
        "message": "Login i suksesshme",
        "device": {
            "mac_address": mac,
            "device_key": key,
            "status": "active",
            "expiry_date": "Unlimited"
        }
    }