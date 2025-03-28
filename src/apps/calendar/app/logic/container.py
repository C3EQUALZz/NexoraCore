import logging
from typing import cast

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from authx import AuthXConfig, AuthX
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

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.consumers.manager import ConsumerManager
from app.infrastructure.brokers.consumers.users import UserDeletedConsumer, UserCreatedConsumer, UserUpdatedConsumer
from app.infrastructure.brokers.kafka import KafkaMessageBroker
from app.infrastructure.uow.events.alchemy import SQLAlchemyEventsUnitOfWork
from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.meetings import CreateMeetingCommand, DeleteMeetingCommand, UpdateMeetingCommand
from app.logic.commands.tasks import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand
from app.logic.events.user import UserDeletedEvent, UserCreatedEvent, UserUpdatedEvent
from app.logic.handlers.meetings.commands import CreateMeetingCommandHandler, DeleteMeetingCommandHandler, \
    UpdateMeetingCommandHandler
from app.logic.handlers.tasks.commands import CreateTaskCommandHandler, UpdateTaskCommandHandler, \
    DeleteTaskCommandHandler
from app.logic.handlers.users.events import UserDeletedEventHandler, UserCreatedEventHandler, UserUpdatedEventHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping
from app.logic.types.handlers import UT
from app.settings.config import Settings, get_settings

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
                CreateTaskCommand: CreateTaskCommandHandler,
                UpdateTaskCommand: UpdateTaskCommandHandler,
                DeleteTaskCommand: DeleteTaskCommandHandler,
                CreateMeetingCommand: CreateMeetingCommandHandler,
                DeleteMeetingCommand: DeleteMeetingCommandHandler,
                UpdateMeetingCommand: UpdateMeetingCommandHandler
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
                UserDeletedEvent: [UserDeletedEventHandler],
                UserCreatedEvent: [UserCreatedEventHandler],
                UserUpdatedEvent: [UserUpdatedEventHandler],
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
                group_id=f"calendar-service-group",
                metadata_max_age_ms=30000,
            ),
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_events_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> EventsUnitOfWork:
        return SQLAlchemyEventsUnitOfWork(session_factory=session_maker)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            broker: BaseMessageBroker,
            uow: UT
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"broker": broker}
        )

    @provide(scope=Scope.APP)
    async def get_consumer_manager(
            self,
            broker: BaseMessageBroker,
            uow: EventsUnitOfWork,
    ) -> ConsumerManager:
        return ConsumerManager(
            consumers=[
                UserDeletedConsumer(broker=broker, uow=uow),
                UserCreatedConsumer(broker=broker, uow=uow),
                UserUpdatedConsumer(broker=broker, uow=uow),
            ]
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


class AuthProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_config(self, settings: Settings) -> AuthXConfig:
        return AuthXConfig(
            JWT_ALGORITHM="RS256",
            JWT_DECODE_ALGORITHMS=["RS256"],
            JWT_PUBLIC_KEY=settings.auth.public_key
        )

    @provide(scope=Scope.APP)
    async def get_security(self, config: AuthXConfig) -> AuthX:
        return AuthX(config=config)


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    BrokerProvider(),
    AppProvider(),
    AuthProvider(),
    context={
        Settings: get_settings(),
    }
)
