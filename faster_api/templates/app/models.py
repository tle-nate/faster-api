"""Models for <<APP_NAME>>."""
import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime

# Import Base declarative class
from app.core.db.base import Base

# TODO: Define your models below.
# Example:
# class MyModel(Base):
#     __tablename__ = "my_model"
#
#     id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
#    updated_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
