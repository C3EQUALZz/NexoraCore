import logging
from typing import cast, Any

from dishka import (
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.uow.teams.base import TeamsUnitOfWork
from app.infrastructure.uow.teams.mongo import MotorTeamsUnitOfWork
from app.logic.commands.team import CreateTeamCommand, UpdateTeamCommand, DeleteTeamCommand
from app.logic.commands.team_members import CreateTeamMemberCommand, UpdateTeamMemberCommand, DeleteTeamMemberCommand
from app.logic.handlers.team_members.commands import CreateTeamMemberCommandHandler, UpdateTeamMemberCommandHandler, \
    DeleteTeamMemberCommandHandler
from app.logic.handlers.teams.commands import CreateTeamCommandHandler, UpdateTeamCommandHandler, \
    DeleteTeamCommandHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping
from app.settings.config import Settings

logger = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            CommandHandlerMapping,
            {
                CreateTeamMemberCommand: CreateTeamMemberCommandHandler,
                UpdateTeamMemberCommand: UpdateTeamMemberCommandHandler,
                DeleteTeamMemberCommand: DeleteTeamMemberCommandHandler,
                CreateTeamCommand: CreateTeamCommandHandler,
                UpdateTeamCommand: UpdateTeamCommandHandler,
                DeleteTeamCommand: DeleteTeamCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(EventHandlerMapping, {})


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_motor_client(self, settings: Settings) -> AsyncIOMotorClient[Any]:
        client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(str(settings.database.url))

        if info := await client.server_info():
            logger.debug("Successfully connected to MongoDB, info [%s]", info)

        return client

    @provide(scope=Scope.APP)
    async def get_teams_motor_uow(self, settings: Settings, client: AsyncIOMotorClient[Any]) -> TeamsUnitOfWork:
        return MotorTeamsUnitOfWork(client=client, database_name=settings.database.name)


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    context={
        Settings: Settings(),
    }
)
