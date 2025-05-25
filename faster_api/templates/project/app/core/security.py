"""Security utilities for password hashing and JWT management."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Tuple

from app.core.config import settings
from jose import JWTError, jwt
from passlib.context import CryptContext

# static pepper for password hashing
_PEPPER = settings.password_pepper

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__type="ID",
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed counterpart using pepper."""
    return pwd_context.verify(plain_password + _PEPPER, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password with pepper for secure storage."""
    return pwd_context.hash(password + _PEPPER)


def create_access_token(data: Dict[str, Any]) -> Tuple[str, datetime]:
    """Create a JWT access token with expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return (encoded_jwt, expire)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a new JWT refresh token with a unique identifier."""
    to_encode = data.copy()
    # include a unique JWT ID to ensure tokens differ even with same payload
    import uuid
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + \
        timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh", "jti": jti})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception: Exception, token_type: str) -> Dict[str, Any]:
    """Decode and verify a JWT token, raising an exception on failure."""
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        if payload.get("type") != token_type:
            raise JWTError()
        return payload
    except JWTError:
        raise credentials_exception
