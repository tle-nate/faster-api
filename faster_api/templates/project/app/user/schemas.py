
"""Pydantic schemas for Preferences."""
from datetime import datetime
from typing import Optional

from app.auth.schemas import User, UserBase, UserCreate  # type: ignore
from pydantic import BaseModel


class PreferencesBase(BaseModel):
    """Base schema for user preferences."""
    pass


class PreferencesCreate(PreferencesBase):
    """Schema for creating user preferences."""
    pass


class Preferences(PreferencesBase):
    """Schema representing user preferences with metadata."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    """Base schema for user profile."""
    timezone: Optional[str] = None
    locale: Optional[str] = None


class ProfileCreate(ProfileBase):
    """Schema for creating user profile."""
    pass


class Profile(ProfileBase):
    """Schema representing user profile with metadata."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
