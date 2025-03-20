import logging

import httpx

from app.domain.entities.user import UserEntity
from app.domain.values.user import Email, Role
from app.infrastructure.clients.base import BaseClient

logger = logging.getLogger(__name__)


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

        return UserEntity(email=Email(response_json.get('email')), role=Role(response_json.get('role')))
