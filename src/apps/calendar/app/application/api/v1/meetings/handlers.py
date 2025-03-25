from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette import status

from app.application.api.v1.meetings.schemas import (
    CreateMeetingSchemaRequest,
    MeetingSchemaResponse,
    UpdateMeetingSchemaRequest
)

from app.domain.entities.events.meeting import MeetingEntity
from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.meetings import DeleteMeetingCommand, CreateMeetingCommand, UpdateMeetingCommand
from app.logic.message_bus import MessageBus
from app.logic.views.meetings import MeetingsView

router = APIRouter(
    prefix="/meetings",
    tags=["meetings"],
    route_class=DishkaRoute
)


@router.get(
    "/{meeting_id}/",
    description="Get meeting in calendar",
    status_code=status.HTTP_200_OK
)
async def get_meeting_in_calendar(
        meeting_id: UUID,
        uow: FromDishka[EventsUnitOfWork]
) -> MeetingSchemaResponse:
    view: MeetingsView = MeetingsView(uow=uow)
    meeting: MeetingEntity = await view.get_meeting_by_id(str(meeting_id))
    return MeetingSchemaResponse.from_entity(meeting)


@router.get(
    "/",
    description="Get all meetings in calendar",
    status_code=status.HTTP_200_OK
)
async def get_all_meetings_in_calendar(
        uow: FromDishka[EventsUnitOfWork],
        page_number: int = Query(1, ge=1, description="Number of page"),
        page_size: int = Query(10, ge=1, description="Size of page")
) -> list[MeetingSchemaResponse]:
    view: MeetingsView = MeetingsView(uow=uow)
    meetings: list[MeetingEntity] = await view.get_all_meetings(page_number=page_number, page_size=page_size)
    return [MeetingSchemaResponse.from_entity(x) for x in meetings]


@router.post(
    "/",
    description="Create new meeting in calendar",
    status_code=status.HTTP_201_CREATED
)
async def create_meeting_in_calendar(
        schema: CreateMeetingSchemaRequest,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> MeetingSchemaResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(CreateMeetingCommand(**schema.model_dump()))
    return MeetingSchemaResponse.from_entity(message_bus.command_result)


@router.put(
    "/{meeting_id}/",
    description="Update meeting in calendar",
    status_code=status.HTTP_200_OK
)
async def update_meeting_in_calendar(
        meeting_id: UUID,
        schema: UpdateMeetingSchemaRequest,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> MeetingSchemaResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(UpdateMeetingCommand(**{"meeting_id": meeting_id, **schema.model_dump()}))
    return MeetingSchemaResponse.from_entity(message_bus.command_result)


@router.delete(
    "/{meeting_id}/",
    description="Delete meeting in calendar",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_meeting_in_calendar(
        meeting_id: UUID,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> None:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(DeleteMeetingCommand(oid=str(meeting_id)))
    return message_bus.command_result
