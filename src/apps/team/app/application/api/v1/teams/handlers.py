import logging
from uuid import UUID
from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.params import Query

from app.application.api.v1.teams.schemas import CreateTeamSchemaRequest, TeamResponse, UpdateTeamSchemaRequest
from app.domain.entities.team import TeamEntity
from app.exceptions.base import ApplicationException
from app.logic.bootstrap import Bootstrap
from app.logic.commands.team import CreateTeamCommand, DeleteTeamCommand, UpdateTeamCommand
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import EventHandlerMapping, CommandHandlerMapping
from app.infrastructure.uow.teams.base import TeamsUnitOfWork
from app.logic.views.teams import TeamsView

router = APIRouter(tags=["teams"], route_class=DishkaRoute)
logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=201,
    description="Handler for creating a new team",
)
async def create_team(
        schema: CreateTeamSchemaRequest,
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> TeamResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(CreateTeamCommand(**schema.model_dump()))

        return TeamResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.get(
    "/",
    status_code=200,
    description="Handler for getting all teams",
)
async def get_all_teams(
        uow: FromDishka[TeamsUnitOfWork],
        page_number: int = Query(1, ge=1, description="Number of page"),
        page_size: int = Query(10, ge=1, description="Size of page")
) -> list[TeamResponse]:
    try:
        teams_view: TeamsView = TeamsView(uow=uow)
        teams: list[TeamEntity] = await teams_view.get_all_teams(page_number=page_number, page_size=page_size)
        return [TeamResponse.from_entity(x) for x in teams]
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.get(
    "/{team_id}/",
    status_code=200,
    description="Handler for getting info about team",
)
async def get_team(
        uow: FromDishka[TeamsUnitOfWork],
        team_id: UUID
) -> TeamResponse:
    try:
        teams_view: TeamsView = TeamsView(uow=uow)
        team = await teams_view.get_team_by_id(str(team_id))
        return TeamResponse.from_entity(team)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.put(
    "/{team_id}/",
    status_code=200,
    description="Handler for updating info about team",
)
async def update_team(
        schema: UpdateTeamSchemaRequest,
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> TeamResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(UpdateTeamCommand(**schema.model_dump()))

        return TeamResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.delete(
    "/{team_id}/",
    status_code=204,
    description="Handler for deleting info about team",
)
async def delete_team(
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping],
        team_id: UUID
) -> None:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(DeleteTeamCommand(oid=str(team_id)))

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))
