"""Pydantic schemas for Profile."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema with shared user attributes."""
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation, including password."""
    password: str


class User(UserBase):
    """Schema for user retrieval with additional metadata."""
    id: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT access token response."""
    access_token: str
    expiry: int
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload validation."""
    sub: str
    exp: int
    type: str


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str
