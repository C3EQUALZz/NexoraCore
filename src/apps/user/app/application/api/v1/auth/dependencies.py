import logging

from authx import AuthX, TokenPayload, RequestToken
from authx.exceptions import AuthXException
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app.exceptions.application import EmptyCredentialsException
from app.logic.container import container

logger = logging.getLogger(__name__)
http_bearer = HTTPBearer(auto_error=False)


async def get_access_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayload:
    security: AuthX = await container.get(AuthX)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(
            token=credentials.credentials,
            location="headers",
            type="access"
        ))

        return payload

    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_refresh_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayload:
    security: AuthX = await container.get(AuthX)

    if credentials is None:
        raise EmptyCredentialsException

    try:
        payload = security.verify_token(RequestToken(
            token=credentials.credentials,
            location="headers",
            type="refresh"
        ))
        return payload

    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
