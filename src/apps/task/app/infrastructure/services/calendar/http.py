import logging
from datetime import datetime
from typing import override

from app.exceptions.infrastructure import NoSuchFieldException, ClientHTTPException, UserNotFoundException, \
    ClientConnectionException, CalendarServiceUnAvailableException
from app.infrastructure.clients.base import BaseClient
from app.infrastructure.services.calendar.base import CalendarService

logger = logging.getLogger(__name__)


class HTTPCalendarService(CalendarService):
    def __init__(self, base_path: str, client: BaseClient):
        self._base_url = base_path
        self._client = client

    @override
    async def is_user_is_available_for_period(
            self,
            user_oid: str,
            start_time: datetime,
            end_time: datetime,
    ) -> bool:

        url: str = f"{self._base_url}/users/{user_oid}/availability"

        params = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        try:
            response = await self._client.get(url, params=params)
            return response.json()["is_available"]
        except KeyError as e:
            logger.error("No such field: %s", e.args[0])
            raise NoSuchFieldException(e.args[0]) from e

        except ClientHTTPException as e:
            if "404" in str(e):
                raise UserNotFoundException(user_oid)
            raise

        except ClientConnectionException as e:
            logger.error("Cannot connect to calendar service: %s", e.url)
            raise CalendarServiceUnAvailableException() from e
