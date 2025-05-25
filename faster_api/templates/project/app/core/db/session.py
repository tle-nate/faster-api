"""Database session and engine."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.pool import StaticPool

# For SQLite (including in-memory), use StaticPool to ensure the same connection across threads
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # For other databases, default engine
    engine = create_engine(
        settings.database_url,
        connect_args={},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)