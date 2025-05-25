"""User model."""
import uuid
from datetime import datetime

from app.core.db.base import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class User(Base):
    """Database model for user accounts."""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RefreshToken(Base):
    """Database model for refresh tokens."""
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
