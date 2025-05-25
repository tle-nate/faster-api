"""API Router for version 1."""
from fastapi import APIRouter

from app.auth import views as auth_views
from app.user import views as user_views

api_router = APIRouter()
api_router.include_router(auth_views.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user_views.router, prefix="/user", tags=["User"])