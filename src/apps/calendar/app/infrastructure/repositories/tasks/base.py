from abc import abstractmethod, ABC

from app.domain.entities.events.task import TaskEntity
from app.infrastructure.repositories.base import AbstractRepository


class TasksRepository(AbstractRepository[TaskEntity], ABC):
    """
    Интерфейс работы с задачами.
    """

    @abstractmethod
    async def get_by_assignee_id(self, assignee_id: str) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_assignee_id_and_status(self, assignee_id: str, status: str) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: str, start: int | None = None, limit: int | None = None) -> list[TaskEntity]:
        raise NotImplementedError
