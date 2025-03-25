import logging
from typing import Self

from app.infrastructure.repositories.task.base import TasksRepository
from app.infrastructure.repositories.task.mongo import MotorTasksRepository
from app.infrastructure.uow.base import MotorAbstractUnitOfWork
from app.infrastructure.uow.task.base import TasksUnitOfWork

logger = logging.getLogger(__name__)


class MotorTeamsUnitOfWork(MotorAbstractUnitOfWork, TasksUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()

        if self._database is None:
            logger.error("Database does not exist")
            raise RuntimeError("Database does not exist")

        self.tasks: TasksRepository = MotorTasksRepository(
            collection=self._database.get_collection("tasks"),
            session=self._session
        )

        return uow
