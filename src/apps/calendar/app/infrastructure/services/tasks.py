from datetime import datetime
from typing import overload

from app.domain.entities.events.task import TaskEntity
from app.exceptions.infrastructure import TaskNotFoundException, AttributeException, PoorTimeException
from app.infrastructure.uow.events.base import EventsUnitOfWork


class TasksService:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, task: TaskEntity) -> TaskEntity:
        async with self._uow as uow:
            new_task: TaskEntity = await uow.tasks.add(task)
            await uow.commit()
            return new_task

    async def get_by_oid(self, task_id: str) -> TaskEntity:
        async with self._uow as uow:
            return await uow.tasks.get(task_id)

    async def update(self, oid: str, task: TaskEntity) -> TaskEntity:
        async with self._uow as uow:
            old_task: TaskEntity | None = await uow.tasks.get(oid)

            if not old_task:
                raise TaskNotFoundException(oid)

            task: TaskEntity | None = await uow.tasks.update(oid, task)

            await uow.commit()

            return task

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            task: TaskEntity | None = await uow.tasks.get(oid)

            if not task:
                raise TaskNotFoundException(oid)

            await uow.tasks.delete(oid)

            await uow.commit()

    async def check_existence(
            self,
            oid: str | None = None,
            assignee_id: str | None = None,
            status: str | None = None,
    ) -> bool:
        if not (oid or (assignee_id and status)):
            raise AttributeException("Please provide oid or assignee_id and status existence checking")

        async with self._uow as uow:
            task: TaskEntity | None

            if assignee_id:
                task: TaskEntity | None = await uow.tasks.get_by_assignee_id(assignee_id)
                if task:
                    return True

            if oid:
                team: TaskEntity | None = await uow.tasks.get(oid)
                if team:
                    return True

            return False

    @overload
    async def get_all(self) -> list[TaskEntity]:
        ...

    @overload
    async def get_all(self, start: int | None, limit: int | None) -> list[TaskEntity]:
        ...

    async def get_all(self, start: int | None = None, limit: int | None = None) -> list[TaskEntity]:
        async with self._uow as uow:
            return await uow.tasks.list(start=start, limit=limit)

    async def is_user_available(self, user_id: str, start_time: datetime, end_time: datetime) -> bool:
        if start_time > end_time:
            raise PoorTimeException

        async with self._uow as uow:
            return await uow.tasks.is_user_available_for_this_time(user_id, start_time, end_time)
