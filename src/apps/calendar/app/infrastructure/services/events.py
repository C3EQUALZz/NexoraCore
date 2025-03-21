from app.domain.entities.events.meeting import MeetingEntity
from app.domain.entities.events.task import TaskEntity
from app.infrastructure.uow.events.base import EventsUnitOfWork


class EventsService:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def add_task(self, task: TaskEntity) -> TaskEntity:
        async with self._uow as uow:
            new_task: TaskEntity = await uow.tasks.add(task)
            await uow.commit()
            return new_task

    async def add_meeting(self, meeting: MeetingEntity) -> MeetingEntity:
        async with self._uow as uow:
            new_meeting: MeetingEntity = await uow.meetings.add(meeting)
            await uow.commit()
            return new_meeting

    async def get_meeting_by_oid(self, meeting_id: str) -> MeetingEntity:
        async with self._uow as uow:
            return await uow.meetings.get(meeting_id)

    async def get_task_by_oid(self, task_id: str) -> TaskEntity:
        async with self._uow as uow:
            return await uow.tasks.get(task_id)
