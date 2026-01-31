import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ky rresht rregullon gabimet e importeve ne Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importimi i moduleve nga folderi app/api
try:
    from app.api.m3u import router as m3u_router
    from app.api.xtream import router as xtream_router
    from app.api.stalker import router as stalker_router
except ImportError as e:
    print(f"GABIM NE IMPORTIM: {e}")
    raise e

# -----------------------
# Database setup (I SIGURT)
# -----------------------
# Tani kodi e merr lidhjen nga 'Environment Variables' ne Render
DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    print("KUJDES: DATABASE_URL nuk u gjet!")

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI(
    title="IPTV Backend API",
    description="API per IPTV",
    version="1.0.0",
)

# -----------------------
# CORS (Lejon frontend-in te lidhet)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Lidhja e rrugëve (Routes)
# -----------------------
app.include_router(m3u_router, prefix="/api/m3u", tags=["m3u"])
app.include_router(stalker_router, prefix="/api/stalker", tags=["stalker"])
app.include_router(xtream_router, prefix="/api/xtream", tags=["xtream"])

@app.get("/")
def root():
    return {
        "status": "Online",
        "message": "IPTV Backend po punon shkelqyeshem!",
        "docs": "/docs"
    }