from abc import ABC, abstractmethod

from app.domain.entities.events.meeting import MeetingEntity
from app.infrastructure.repositories.base import AbstractRepository


class MeetingsRepository(AbstractRepository[MeetingEntity], ABC):
    """
    Интерфейс работы с встречами.
    """

    @abstractmethod
    async def add(self, model: MeetingEntity) -> MeetingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> MeetingEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: MeetingEntity) -> MeetingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_organizer_id(self, organizer_id: str) -> list[MeetingEntity]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_participant_id(
            self,
            participant_id: str,
            start: int | None = None,
            limit: int | None = None
    ) -> list[MeetingEntity]:
        raise NotImplementedError

    @abstractmethod
    async def list(
            self,
            start: int | None = None,
            limit: int | None = None
    ) -> list[MeetingEntity]:
        raise NotImplementedError
