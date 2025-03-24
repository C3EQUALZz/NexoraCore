from abc import ABC, abstractmethod
from app.infrastructure.repositories.base import AbstractRepository
from app.domain.entities.calendar import CalendarEntity


class CalendarsRepository(AbstractRepository[CalendarEntity], ABC):
    """
    Интерфейс работы с календарями.
    """

    @abstractmethod
    async def get_by_owner_id(self, owner_id: str) -> CalendarEntity | None:
        raise NotImplementedError
