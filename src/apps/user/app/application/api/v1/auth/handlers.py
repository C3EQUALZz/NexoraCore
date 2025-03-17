import logging
from typing import Annotated

from authx import AuthX, TokenPayload, RequestToken
from authx.exceptions import AuthXException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from starlette import status
from starlette.requests import Request

from app.application.api.v1.auth.schemas import TokenResponse
from app.application.api.v1.users.schemas import UserSchemaResponse
from app.domain.entities.user import UserEntity
from app.exceptions.base import ApplicationException
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.message_bus import MessageBus
from app.logic.views.users import UsersViews

logger = logging.getLogger(__name__)
bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute, dependencies=[Depends(bearer)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user logging",
)
async def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]],
        security: FromDishka[AuthX]
) -> TokenResponse:
    try:
        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(VerifyUserCredentialsCommand(email=form.username, password=form.password))
        user: UserEntity = messagebus.command_result

        return TokenResponse(
            access_token=security.create_access_token(uid=str(user.oid)),
            refresh_token=security.create_refresh_token(uid=str(user.oid)),
        )

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message, headers={"WWW-Authenticate": "Bearer"})


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    summary="Endpoint for user refreshing",
)
async def refresh(
        security: FromDishka[AuthX],
        token: str = Depends(oauth2_scheme),
) -> TokenResponse:
    try:
        refresh_token_payload = security.verify_token(token=RequestToken(token=token, location="headers"))
        return TokenResponse(access_token=security.create_access_token(refresh_token_payload.sub))
    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    summary="Endpoint for user info",
    dependencies=[Depends(oauth2_scheme)],
)
async def get_me(
        security: FromDishka[AuthX],
        request: Request,
        uow: FromDishka[UsersUnitOfWork],
) -> UserSchemaResponse:
    try:
        access_token: TokenPayload = await security.access_token_required(request)

        users_views: UsersViews = UsersViews(uow=uow)
        user: UserEntity = await users_views.get_user_by_id(access_token.sub)
        return UserSchemaResponse.from_entity(entity=user)

    except AuthXException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=e.message)
