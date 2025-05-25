"""Main application module for FastAPI server."""
import os 
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv 
load_dotenv()

from app.core.db.base import Base
from app.core.db.session import engine
from app.core.config import settings 
from app.core.routers.v1 import api_router as api_router

app = FastAPI(
    title=settings.app_name,
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS to allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"]   # Allows all headers
)

@app.get("/", tags=["Health Check"])
def health_check() -> dict[str, str]:
    """Health check endpoint returning welcome message."""
    return {"message": f"Welcome to {settings.app_name}"}

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on application startup."""
    Base.metadata.create_all(bind=engine)

