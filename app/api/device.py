from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db

router = APIRouter()

# ─── Model ──────────────────────────────────────────────────
class DeviceVerifyRequest(BaseModel):
    mac_address: str
    device_key: str

# ─── POST /verify ───────────────────────────────────────────
@router.post("/verify")
async def verify_device(request: DeviceVerifyRequest):
    mac = request.mac_address.strip().upper()
    key = request.device_key.strip()

    if not mac or not key:
        raise HTTPException(status_code=400, detail="MAC address dhe device key janë detyrimshme!")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices WHERE mac_address = ? AND device_key = ?", (mac, key))
    device = cursor.fetchone()
    conn.close()

    if not device:
        raise HTTPException(status_code=401, detail="MAC address ose device key i gauar!")

    return {
        "success": True,
        "message": "Login i suksesshme",
        "device": {
            "mac_address": device["mac_address"],
            "device_key": device["device_key"],
            "status": device["status"],
            "expiry_date": device["expiry_date"] if device["expiry_date"] else "Unlimited"
        }
    }