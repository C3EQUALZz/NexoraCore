import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Query

from app.application.api.v1.team_members.schemas import CreateTeamMemberSchemaRequest, TeamMemberSchemaResponse
from app.domain.entities.team_members import TeamMemberEntity
from app.exceptions.base import ApplicationException
from app.infrastructure.uow.teams.base import TeamsUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.team_members import CreateTeamMemberCommand, DeleteTeamMemberCommand
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import EventHandlerMapping, CommandHandlerMapping
from app.logic.views.team_members import TeamMembersView

router = APIRouter(prefix="/{team_id}/members", tags=["team_members"], route_class=DishkaRoute)
logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=201,
    description="Add user to the team",
)
async def create_team_member(
        team_id: UUID,
        schema: CreateTeamMemberSchemaRequest,
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> TeamMemberSchemaResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(CreateTeamMemberCommand(**{"team_id": str(team_id), **schema.model_dump()}))

        return TeamMemberSchemaResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.get(
    "/",
    status_code=200,
    description="Get all members in team",
)
async def get_all_team_members(
        team_id: UUID,
        uow: FromDishka[TeamsUnitOfWork],
        page_number: int = Query(1, ge=1, description="Number of page"),
        page_size: int = Query(10, ge=1, description="Size of page")
) -> list[TeamMemberSchemaResponse]:
    try:
        team_members_view: TeamMembersView = TeamMembersView(uow=uow)
        all_team_members: list[TeamMemberEntity] = await team_members_view.get_all_team_members_in_team(
            team_id=str(team_id),
            page_number=page_number,
            page_size=page_size
        )

        return [TeamMemberSchemaResponse.from_entity(x) for x in all_team_members]
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.get(
    "/{user_id}/",
    status_code=200,
    description="Getting user in team",
)
async def get_user_info(
        team_id: UUID,
        user_id: UUID,
        uow: FromDishka[TeamsUnitOfWork]
) -> TeamMemberSchemaResponse:
    try:
        team_members_view: TeamMembersView = TeamMembersView(uow=uow)
        user: TeamMemberEntity = await team_members_view.get_by_user_id(team_id=str(team_id), user_id=str(user_id))
        return TeamMemberSchemaResponse.from_entity(user)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.delete(
    "/{user_id}/",
    status_code=204,
    description="Delete a team member"
)
async def delete_team_member(
        team_id: UUID,
        user_id: UUID,
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> None:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(DeleteTeamMemberCommand(team_id=str(team_id), user_id=str(user_id)))

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.put(
    "/{user_id}/",
    status_code=200,
)
async def update_team_member(user_id: str):
    ...
