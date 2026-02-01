from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ─── Model ──────────────────────────────────────────────────
class DeviceVerifyRequest(BaseModel):
    mac_address: str
    device_key: str

# ─── Devices te hardcoded ───────────────────────────────────
# Shto MAC address dhe device_key te pajisjes tuaj ketu
DEVICES = {
    "C6:7B:43:74:68:6E": "TEST1234",
}

# ─── POST /verify ───────────────────────────────────────────
@router.post("/verify")
async def verify_device(request: DeviceVerifyRequest):
    mac = request.mac_address.strip().upper()
    key = request.device_key.strip()

    if not mac or not key:
        raise HTTPException(status_code=400, detail="MAC address dhe device key janë detyrimshme!")

    # Kontrollim nese device ekziston dhe key eshte i saktë
    if mac not in DEVICES:
        raise HTTPException(status_code=401, detail="MAC address i gauar!")

    if DEVICES[mac] != key:
        raise HTTPException(status_code=401, detail="Device key i gauar!")

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