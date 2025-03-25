import asyncio

from app.domain.entities.events.meeting import MeetingEntity
from app.domain.entities.user import UserEntity
from app.infrastructure.services.meetings import MeetingsService
from app.infrastructure.services.user import UserService
from app.logic.commands.meetings import CreateMeetingCommand, DeleteMeetingCommand, UpdateMeetingCommand
from app.logic.handlers.meetings.base import MeetingsCommandHandler


class CreateMeetingCommandHandler(MeetingsCommandHandler[CreateMeetingCommand]):
    async def __call__(self, command: CreateMeetingCommand) -> MeetingEntity:
        user_service: UserService = UserService(uow=self._uow)
        meeting_service: MeetingsService = MeetingsService(uow=self._uow)

        organizer: UserEntity = await user_service.get_by_id(command.organizer_id)

        participants: list[UserEntity] = await asyncio.gather(
            *(user_service.get_by_id(x) for x in command.participant_ids)
        )

        meeting: MeetingEntity = MeetingEntity(
            organizer=organizer,
            participants=participants,
            title=command.title,
            description=command.description,
        )

        return await meeting_service.add(meeting)


class DeleteMeetingCommandHandler(MeetingsCommandHandler[DeleteMeetingCommand]):
    async def __call__(self, command: DeleteMeetingCommand) -> None:
        meeting_service: MeetingsService = MeetingsService(uow=self._uow)
        return await meeting_service.delete(oid=command.oid)


class UpdateMeetingCommandHandler(MeetingsCommandHandler[UpdateMeetingCommand]):
    async def __call__(self, command: UpdateMeetingCommand) -> MeetingEntity:
        user_service: UserService = UserService(uow=self._uow)
        meeting_service: MeetingsService = MeetingsService(uow=self._uow)

        organizer: UserEntity = await user_service.get_by_id(command.organizer_id)

        participants: list[UserEntity] = await asyncio.gather(
            *(user_service.get_by_id(x) for x in command.participant_ids)
        )

        meeting: MeetingEntity = MeetingEntity(
            organizer=organizer,
            participants=participants,
            title=command.title,
            description=command.description,
        )

        return await meeting_service.update(oid=command.oid, meeting=meeting)
