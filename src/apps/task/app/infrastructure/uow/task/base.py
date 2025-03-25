from abc import ABC

from app.infrastructure.repositories.task.base import TasksRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class TasksUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with teams, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    tasks: TasksRepository
