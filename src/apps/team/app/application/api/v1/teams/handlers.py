import logging

from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.application.api.v1.teams.schemas import CreateTeamSchemaRequest
from app.exceptions.base import ApplicationException
from app.logic.bootstrap import Bootstrap
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import EventHandlerMapping, CommandHandlerMapping
from app.infrastructure.uow.teams.base import TeamsUnitOfWork

router = APIRouter(tags=["teams"], route_class=DishkaRoute)
logger = logging.getLogger(__name__)


@router.post(
    "",
    status_code=201,
    description="Handler for creating a new team",
)
async def create_team(
        schema: CreateTeamSchemaRequest,
        uow: FromDishka[TeamsUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
):
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow, events_handlers_for_injection=events, commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(CreateTeamCommand(**schema.model_dump()))

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))

@router.get(
    "/{team_id}",
    status_code=200,
    description="Handler for getting info about team",
)
async def get_team(team_id: str):
    ...


@router.put(
    "/{team_id}",
    status_code=200,
    description="Handler for updating info about team",
)
async def update_team(team_id: str):
    ...


@router.delete(
    "/{team_id}",
    status_code=204,
    description="Handler for deleting info about team",
)
async def delete_team(team_id: str):
    ...
