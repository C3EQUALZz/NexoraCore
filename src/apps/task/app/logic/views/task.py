from app.domain.entities.task import TaskEntity
from app.infrastructure.services.task import TasksService
from app.infrastructure.uow.task.base import TasksUnitOfWork


class TasksView:
    def __init__(self, uow: TasksUnitOfWork) -> None:
        self._uow = uow

    async def get_task_by_id(self, task_id: str) -> TaskEntity:
        tasks_service: TasksService = TasksService(self._uow)
        return await tasks_service.get_by_task_id(task_id)