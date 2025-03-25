import logging

from app.domain.entities.user import UserEntity
from app.domain.values.user import Role, Email
from app.exceptions.infrastructure import UserNotFoundException, NoSuchFieldException, \
    ClientHTTPException, ClientConnectionException, CalendarServiceUnAvailableException
from app.infrastructure.clients.base import BaseClient, ClientResponse
from app.infrastructure.services.user.base import UserService

logger = logging.getLogger(__name__)


class HttpUserService(UserService):
    def __init__(self, client: BaseClient, base_path: str) -> None:
        self._client: BaseClient = client
        self._base_path: str = base_path

    async def get_user(self, user_oid: str) -> UserEntity:
        url: str = f"{self._base_path}/{user_oid}/"

        try:
            response: ClientResponse = await self._client.get(url)
            if response.status_code == 404:
                raise UserNotFoundException(user_oid)

            user_data = response.json()

            return UserEntity(
                oid=user_data["oid"],
                role=Role(user_data["role"]),
                email=Email(user_data["email"]),
            )

        except KeyError as e:
            logger.error("No such field: %s", e.args[0])
            raise NoSuchFieldException(e.args[0]) from e

        except ClientHTTPException as e:
            if "404" in str(e):
                raise UserNotFoundException(user_oid)
            raise

        except ClientConnectionException as e:
            logger.error("Cannot connect to calendar service: %s", e.url)
            raise CalendarServiceUnAvailableException from e

    async def close(self) -> None:
        await self._client.close()
