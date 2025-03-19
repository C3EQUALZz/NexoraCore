import httpx
import logging
from app.exceptions.infrastructure import EmptyJsonResponseException, EmptyRoleFieldInJsonException
from app.infrastructure.clients.base import BaseClient

logger = logging.getLogger(__name__)

class UserClientService:
    """Клиент микросервиса Users."""

    def __init__(self, url: str, client: BaseClient) -> None:
        self._url = url
        self._client = client

    async def get_user_role(self, user_oid: str) -> str:
        user_json = await self.get_user(user_oid)

        if user_json is None:
            raise EmptyJsonResponseException

        if user_json.get('role') is None:
            raise EmptyRoleFieldInJsonException

        return user_json.get('role')


    async def get_user(
            self,
            user_oid: str
    ) -> dict[str, ...] | None:
        """Получить пользователя, если он есть на микросервисе Users через httpx."""
        try:

            url: str = self._url + f"/{user_oid}/"

            response = await self._client.get(url=url)

            logger.info("Making response: %s", url)

            response.raise_for_status()  # Проверка на HTTP ошибки.

            response_json = response.json()  # Конвертируем ответ в json-формат.

        except (httpx.HTTPStatusError, httpx.RequestError):
            return None

        return response_json