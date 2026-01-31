import os
import httpx

XTREAM_API_KEY = os.getenv("XTREAM_API_KEY")
XTREAM_API_BASE_URL = os.getenv("XTREAM_API_BASE_URL")

async def login(username: str, password: str):
    url = f"{XTREAM_API_BASE_URL}/login"
    payload = {"username": username, "password": password, "api_key": XTREAM_API_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        return resp.json()
