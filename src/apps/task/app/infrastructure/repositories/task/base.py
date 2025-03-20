from app.infrastructure.repositories.base import AbstractRepository
from app.domain.entities.task import TaskEntity
from abc import ABC, abstractmethod


class TasksRepository(AbstractRepository[TaskEntity], ABC):
    """
    An interface for work with tasks, that is used by TasksUnitOfWork.
    The main goal is that implementations of this interface can be easily replaced in TasksUnitOfWork
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_title_and_description(self, title: str, description: str) -> TaskEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_assigned_to_and_created_by(self, assigned_to: str, created_by: str) -> TaskEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: TaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> TaskEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[TaskEntity]:
        raise NotImplementedError
