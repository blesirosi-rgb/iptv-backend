

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import routers
from app.api.m3u import router as m3u_router
from app.api.xtream import router as xtream_router
from app.api.stalker import router as stalker_router



# -----------------------
# Database setup
# -----------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://blesio:nretgihTI3bZdKLMMBlvmntbf51N4tDX@dpg-d5ufr9ngi27c7396fes0-a/iptvott_backend"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI(
    title="IPTV Backend API",
    description="API për IPTV me M3U, Stalker dhe Xtream",
    version="1.0.0",
)

# -----------------------
# CORS setup
# -----------------------
origins = [
    "https://blesioiptv.netlify.app",  # domaini yt frontend
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Include routers
# -----------------------
app.include_router(m3u_router, prefix="/api/m3u", tags=["m3u"])
app.include_router(stalker_router, prefix="/api/stalker", tags=["stalker"])
app.include_router(xtream_router, prefix="/api/xtream", tags=["xtream"])

# -----------------------
# Root endpoint
# -----------------------
@app.get("/")
def root():
    return {"message": "IPTV Backend is running!"}
