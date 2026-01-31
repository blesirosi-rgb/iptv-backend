import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Kjo siguron që folderi 'app' të njihet si modul nga Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importimi i router-ave (Sigurohu që skedarët në app/api/ kanë 'router = APIRouter()')
try:
    from app.api.m3u import router as m3u_router
    from app.api.xtream import router as xtream_router
    from app.api.stalker import router as stalker_router
except ImportError as e:
    print(f"GABIM NE IMPORTIM: {e}")
    raise e

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
    "https://blesioiptv.netlify.app",  # Domaini yt frontend
    "http://localhost",
    "http://localhost:3000",
    "*" # Lejon testimin nga çdo vend përkohësisht
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
    return {
        "status": "Online",
        "message": "IPTV Backend is running successfully!",
        "docs": "/docs"
    }