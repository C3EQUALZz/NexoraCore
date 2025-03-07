import logging
from typing import cast

from dishka import (
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.uow.teams.alchemy import SQLAlchemyTeamsUnitOfWork
from app.infrastructure.uow.teams.base import TeamsUnitOfWork
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
    async def get_engine_client(self, settings: Settings) -> AsyncEngine:
        engine: AsyncEngine = create_async_engine(
            url=settings.database.url,
            pool_pre_ping=settings.alchemy_settings.pool_pre_ping,
            pool_recycle=settings.alchemy_settings.pool_recycle,
            echo=settings.alchemy_settings.echo,
        )

        logger.debug("Successfully connected to Database")

        return engine

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine, settings: Settings) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=settings.alchemy_settings.auto_flush,
            expire_on_commit=settings.alchemy_settings.expire_on_commit,
        )

        return session_maker

    @provide(scope=Scope.APP)
    async def get_teams_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> TeamsUnitOfWork:
        return SQLAlchemyTeamsUnitOfWork(session_factory=session_maker)


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    context={
        Settings: Settings(),
    }
)
