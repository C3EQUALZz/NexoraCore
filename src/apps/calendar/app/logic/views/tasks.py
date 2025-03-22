from app.domain.entities.events.task import TaskEntity
from app.infrastructure.services.tasks import TasksService
from app.infrastructure.uow.events.base import EventsUnitOfWork


class TasksView:
    """
    Views related to users, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.
    """

    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow: EventsUnitOfWork = uow

    async def get_task_by_id(self, task_id: str) -> TaskEntity:
        tasks_service: TasksService = TasksService(self._uow)
        task: TaskEntity = await tasks_service.get_by_oid(task_id)
        return task

    async def get_all_tasks(self, page_number: int = 1, page_size: int = 10) -> list[TaskEntity]:
        tasks_service: TasksService = TasksService(self._uow)
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size
        tasks: list[TaskEntity] = await tasks_service.get_all(start=start, limit=limit)
        return tasks

