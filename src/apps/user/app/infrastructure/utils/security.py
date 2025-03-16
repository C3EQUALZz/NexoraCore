import uuid
from datetime import timedelta, datetime, UTC
from typing import Any

import bcrypt
import jwt

from app.settings.config import get_settings, Settings


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def __create_token(
        payload: dict[str, Any],
        time_to_expire: timedelta
) -> str:
    """Private function for creating a jwt token"""
    settings: Settings = get_settings()

    to_encode: dict[str, Any] = payload.copy()

    now: datetime = datetime.now(UTC)
    expire: datetime = now + time_to_expire
    jwt_unique_oid: str = str(uuid.uuid4())

    to_encode.update(exp=expire, iat=now, jti=jwt_unique_oid)

    return jwt.encode(
        payload=to_encode,
        key=settings.auth.private_key,
        algorithm=settings.auth.algorithm,
    )


def create_access_token(
        user_oid: str,
        expires_delta: timedelta | None = None,
) -> str:
    """
    Create JWT access token using unique identifier for user.
    """
    settings: Settings = get_settings()

    payload = {"sub": user_oid, "type": "access"}

    time_to_expire: timedelta = timedelta(minutes=settings.auth.access_token_expire_minutes) + expires_delta

    access_token = __create_token(
        payload=payload,
        time_to_expire=time_to_expire,
    )

    return access_token


def create_refresh_token(
        user_oid: str,
        expires_delta: timedelta | None = None,
) -> str:

    settings: Settings = get_settings()

    payload = {"sub": user_oid, "type": "refresh"}

    time_to_expire: timedelta = timedelta(minutes=settings.auth.refresh_token_expire_minutes) + expires_delta

    refresh_token = __create_token(
        payload=payload,
        time_to_expire=time_to_expire,
    )

    return refresh_token

