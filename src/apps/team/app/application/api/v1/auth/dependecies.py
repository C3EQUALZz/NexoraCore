import logging

from authx import RequestToken, AuthX, TokenPayload
from authx.exceptions import AuthXException
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.exceptions.application import RolePermissionDenyException, EmptyCredentialsException, AuthException
from app.infrastructure.services.user import UserClientService
from app.logic.container import container
from app.settings.config import Settings, get_settings

logger = logging.getLogger(__name__)
http_bearer = HTTPBearer(auto_error=False)

async def get_access_token_payload(
        credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer)
) -> TokenPayload:

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
        raise AuthException(str(e))



class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self._allowed_roles: list[str] = allowed_roles
        self.__settings: Settings = get_settings()

    async def __call__(
            self,
            token: TokenPayload = Depends(get_access_token_payload),
            creds: HTTPAuthorizationCredentials | None = Depends(http_bearer)
    ) -> bool:

        if creds is None:
            raise EmptyCredentialsException

        user_service: UserClientService = await container.get(UserClientService)

        if await user_service.get_user_role(token.sub, creds.credentials, creds.scheme) in self._allowed_roles:
            return True

        raise RolePermissionDenyException
