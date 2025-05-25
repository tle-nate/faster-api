"""CRUD functions for User model."""
import datetime
from typing import Optional

from app.auth.models import RefreshToken
from app.auth.models import User as UserModel
from app.auth.schemas import UserCreate
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: str) -> Optional[UserModel]:
    """Retrieve a user by ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """Retrieve a user by email address."""
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user: UserCreate) -> UserModel:
    """Create a new user with hashed password."""
    from app.core.security import get_password_hash
    db_user = UserModel(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_superuser(db: Session, name: str, email: str, password: str) -> UserModel:
    """Create a new superuser with admin privileges."""
    from app.core.security import get_password_hash
    db_user = UserModel(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        is_admin=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_refresh_token(db: Session, user_id: str, token: str, expires_at: datetime.datetime) -> RefreshToken:
    """Create and persist a new refresh token."""
    db_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_refresh_token(db: Session, token: str) -> Optional[RefreshToken]:
    """Retrieve a refresh token by its token string."""
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(db: Session, db_token: RefreshToken) -> None:
    """Revoke a refresh token by marking it revoked."""
    """Mark a refresh token as revoked."""
    db_token.revoked = True
    db.add(db_token)
    db.commit()
