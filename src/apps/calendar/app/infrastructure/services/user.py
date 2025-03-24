import logging

import httpx

from app.domain.entities.user import UserEntity
from app.domain.values.user import Role
from app.exceptions.infrastructure import UserNotFoundException
from app.infrastructure.clients.base import BaseClient
from app.infrastructure.uow.events.base import EventsUnitOfWork

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            new_user: UserEntity = await uow.users.add(user)
            await uow.commit()
            return new_user

    async def get_by_id(self, oid: str) -> UserEntity:
        async with self._uow as uow:
            user: UserEntity | None = await uow.users.get(oid=oid)

            if not user:
                raise UserNotFoundException(str(oid))

            return user

    async def update(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            updated_user = await uow.users.update(oid=user.oid, model=user)
            await uow.commit()
            return updated_user

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            user: UserEntity | None = await uow.users.get(oid=oid)

            if not user:
                raise UserNotFoundException(str(oid))

            await uow.users.delete(oid)
            await uow.commit()

    async def get_all(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        async with self._uow as uow:
            return await uow.users.list(start=start, limit=limit)


class UserClientService:
    """Клиент микросервиса Users."""

    def __init__(self, url: str, client: BaseClient) -> None:
        self._url = url
        self._client = client

    async def get_user(
            self,
            user_oid: str
    ) -> UserEntity | None:
        """Получить пользователя, если он есть на микросервисе Users через httpx."""

        url: str = self._url + f"/{user_oid}/"

        try:

            response = await self._client.get(url=url)
            logger.info("Making response: %s", url)
            response.raise_for_status()  # Проверка на HTTP ошибки.
            response_json = response.json()  # Конвертируем ответ в json-формат.

        except (httpx.HTTPStatusError, httpx.RequestError):
            logger.error("Bad response: %s", url)
            return None

        return UserEntity(oid=response_json.get('oid'), role=Role(response_json.get('role')))
