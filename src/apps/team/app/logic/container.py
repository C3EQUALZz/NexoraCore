import logging
from typing import cast, Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from authx import AuthXConfig, AuthX
from dishka import (
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from httpx import AsyncHTTPTransport, Limits, Timeout, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.kafka import KafkaMessageBroker
from app.infrastructure.clients.base import BaseClient
from app.infrastructure.clients.http import HTTPXClient
from app.infrastructure.services.user import UserClientService
from app.infrastructure.uow.teams.base import TeamsUnitOfWork
from app.infrastructure.uow.teams.mongo import MotorTeamsUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.team import CreateTeamCommand, UpdateTeamCommand, DeleteTeamCommand
from app.logic.commands.team_members import CreateTeamMemberCommand, UpdateTeamMemberCommand, DeleteTeamMemberCommand, \
    PublishNewTidingCommand
from app.logic.events.team_members import PublishNewTideEvent
from app.logic.handlers.team_members.commands import CreateTeamMemberCommandHandler, UpdateTeamMemberCommandHandler, \
    DeleteTeamMemberCommandHandler, PublishNewTidingCommandHandler
from app.logic.handlers.teams.commands import CreateTeamCommandHandler, UpdateTeamCommandHandler, \
    DeleteTeamCommandHandler
from app.logic.handlers.team_members.events import PublishNewTideEventHandler
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping, UT
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
                CreateTeamMemberCommand: CreateTeamMemberCommandHandler,
                UpdateTeamMemberCommand: UpdateTeamMemberCommandHandler,
                DeleteTeamMemberCommand: DeleteTeamMemberCommandHandler,
                CreateTeamCommand: CreateTeamCommandHandler,
                UpdateTeamCommand: UpdateTeamCommandHandler,
                DeleteTeamCommand: DeleteTeamCommandHandler,
                PublishNewTidingCommand: PublishNewTidingCommandHandler
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(EventHandlerMapping, {
            PublishNewTideEvent: [PublishNewTideEventHandler]
        })


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_motor_client(self, settings: Settings) -> AsyncIOMotorClient[Any]:
        client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(str(settings.database.url))

        if info := await client.server_info():
            logger.debug("Successfully connected to MongoDB, info [%s]", info)

        return client


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_kafka_broker(self, settings: Settings) -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.broker.url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.broker.url,
                group_id=f"team-service-group",
                metadata_max_age_ms=30000,
            ),
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            broker: BaseMessageBroker,
            service: UserClientService,
            uow: UT
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"broker": broker, "service": service}
        )

    @provide(scope=Scope.APP)
    async def get_teams_motor_uow(self, settings: Settings, client: AsyncIOMotorClient[Any]) -> TeamsUnitOfWork:
        return MotorTeamsUnitOfWork(client=client, database_name=settings.database.name)


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


class HTTPProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_http_transport(self, settings: Settings) -> AsyncClient:
        transport: AsyncHTTPTransport = AsyncHTTPTransport(
            limits=Limits(
                max_connections=settings.client.max_connections,
                max_keepalive_connections=settings.client.max_keepalive_connections,
                keepalive_expiry=settings.client.keepalive_expiry,
            )
        )

        return AsyncClient(
            transport=transport, timeout=Timeout(settings.client.timeout)
        )

    @provide(scope=Scope.APP)
    async def get_http_client(self, client: AsyncClient) -> BaseClient:
        return HTTPXClient(client=client)

    @provide(scope=Scope.APP)
    async def get_user_client_service(self, client: BaseClient, settings: Settings) -> UserClientService:
        return UserClientService(client=client, url=settings.client.user_endpoint_url)


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    HTTPProvider(),
    AuthProvider(),
    BrokerProvider(),
    AppProvider(),
    context={
        Settings: get_settings(),
    }
)
