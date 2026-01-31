import os

files = {
    "app/api/__init__.py": "",

    "app/api/m3u.py": """from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
def upload_m3u(url: str):
    return {"status": "ok", "type": "m3u", "url": url}
""",

    "app/api/xtream.py": """from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login(host: str, username: str, password: str):
    return {"status": "ok", "host": host}
""",

    "app/api/stalker.py": """from fastapi import APIRouter

router = APIRouter()

@router.post("/mac")
def mac_login(mac: str, portal: str):
    return {"status": "ok", "mac": mac}
""",

    "app/services/m3u_parser.py": "# M3U parser logic here\n",
    "app/services/xtream_client.py": "# Xtream client logic here\n",
    "app/services/stalker_client.py": "# Stalker client logic here\n",
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Struktura u rregullua dhe file-at u krijuan")
