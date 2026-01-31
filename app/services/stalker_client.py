import os
import httpx

STALKER_API_URL = os.getenv("STALKER_API_URL")
STALKER_API_KEY = os.getenv("STALKER_API_KEY")

async def get_mac_info(mac: str):
    url = f"{STALKER_API_URL}/mac"
    payload = {"mac": mac, "api_key": STALKER_API_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        return resp.json()
