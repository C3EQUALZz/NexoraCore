from app.domain.entities.task import TaskEntity
from app.infrastructure.uow.task.base import TasksUnitOfWork


class TasksService:
    def __init__(self, uow: TasksUnitOfWork) -> None:
        self._uow = uow

    async def add(self, task: TaskEntity) -> TaskEntity:
        ...

    async def get_by_task_id(self, task_id: str) -> TaskEntity | None:
        ...

    async def get_by_title_and_description(self, title: str, description: str) -> TaskEntity:
        ...

    async def get_by_assigned_to_and_created_by(self, assigned_to: str, created_by: str) -> TaskEntity:
        ...

    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        ...

    async def get_all(self, start: int = 0, limit: int = 10) -> list[TaskEntity]:
        ...

    async def delete(self, task_id) -> None:
        ...
