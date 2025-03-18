import logging

from authx import AuthX, TokenPayload, RequestToken
from authx.exceptions import AuthXException
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app.exceptions.application import EmptyCredentialsException, ForbiddenTokenException, \
    AuthException
from app.infrastructure.cache.base import BaseCache
from app.logic.container import container

logger = logging.getLogger(__name__)
http_bearer = HTTPBearer(auto_error=False)


async def get_access_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayload:
    security: AuthX = await container.get(AuthX)
    cache: BaseCache = await container.get(BaseCache)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(
            token=credentials.credentials,
            location="headers",
            type="access"
        ))

        if await cache.get(payload.jti) is not None:
            raise ForbiddenTokenException()

        return payload

    except AuthXException as e:
        raise AuthException(str(e))


async def get_refresh_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayload:
    security: AuthX = await container.get(AuthX)
    cache: BaseCache = await container.get(BaseCache)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(
            token=credentials.credentials,
            location="headers",
            type="refresh"
        ))

        if await cache.get(payload.jti) is not None:
            raise ForbiddenTokenException()

        return payload

    except AuthXException as e:
        raise AuthException(str(e))
