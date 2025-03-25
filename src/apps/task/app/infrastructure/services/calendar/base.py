from abc import ABC, abstractmethod
from datetime import datetime


class CalendarService(ABC):
    """
    Client for calendar microservice
    """

    @abstractmethod
    async def is_user_is_available_for_period(
            self,
            user_oid: str,
            start_time: datetime,
            end_time: datetime,
    ) -> bool:
        """
        Проверяет доступность пользователя в указанный период.

        :param user_oid: UUID of User
        :param start_time: start of period (timezone-aware datetime)
        :param end_time: end of period (timezone-aware datetime)
        """
        ...
