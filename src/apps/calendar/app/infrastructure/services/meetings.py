from app.domain.entities.events.meeting import MeetingEntity
from app.exceptions.infrastructure import MeetingNotFoundException
from app.infrastructure.uow.events.base import EventsUnitOfWork


class MeetingsService:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, meeting: MeetingEntity) -> MeetingEntity:
        async with self._uow as uow:
            new_task: MeetingEntity = await uow.meetings.add(meeting)
            await uow.commit()
            return new_task

    async def get_by_oid(self, meeting_id: str) -> MeetingEntity:
        async with self._uow as uow:
            return await uow.meetings.get(meeting_id)

    async def update(self, oid: str, meeting: MeetingEntity) -> MeetingEntity:
        async with self._uow as uow:
            old_meeting: MeetingEntity | None = await uow.meetings.get(oid)

            if not old_meeting:
                raise MeetingNotFoundException(oid)

            meeting: MeetingEntity | None = await uow.meetings.update(oid, meeting)

            await uow.commit()

            return meeting

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            meeting: MeetingEntity | None = await uow.meetings.get(oid)

            if not meeting:
                raise MeetingNotFoundException(oid)

            await uow.meetings.delete(oid)

            await uow.commit()

    async def get_all(self, start: int | None = None, limit: int | None = None) -> list[MeetingEntity]:
        async with self._uow as uow:
            return await uow.meetings.list(start=start, limit=limit)
