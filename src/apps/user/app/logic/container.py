import logging
from typing import cast

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
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

from app.logic.bootstrap import Bootstrap
from app.logic.types.handlers import UT

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.kafka import KafkaMessageBroker
from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, VerifyUserCredentialsCommand, \
    DeleteUserCommand
from app.logic.events.users import UserDeleteEvent
from app.logic.handlers.users.commands import CreateUserCommandHandler, UpdateUserCommandHandler, \
    VerifyUserCredentialsCommandHandler, DeleteUserCommandHandler
from app.logic.handlers.users.events import UserDeleteEventHandler
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
                CreateUserCommand: CreateUserCommandHandler,
                UpdateUserCommand: UpdateUserCommandHandler,
                VerifyUserCredentialsCommand: VerifyUserCredentialsCommandHandler,
                DeleteUserCommand: DeleteUserCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            EventHandlerMapping,
            {
                UserDeleteEvent: [UserDeleteEventHandler]
            }
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_kafka_broker(self, settings: Settings) -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.broker.url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.broker.url,
                group_id=f"users-service-group",
                metadata_max_age_ms=30000,
            ),
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_users_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> UsersUnitOfWork:
        return SQLAlchemyUsersUnitOfWork(session_factory=session_maker)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            broker: BaseMessageBroker,
            uow: type[UT]
    ) -> Bootstrap[UT]:

        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"broker": broker}
        )


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



container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    BrokerProvider(),
    AppProvider(),
    context={
        Settings: Settings(),
    }
)
