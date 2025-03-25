from typing import cast

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from dishka import Provider, provide, Scope, from_context, make_async_container
from httpx import AsyncClient, AsyncHTTPTransport, Limits, Timeout

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.kafka import KafkaMessageBroker
from app.infrastructure.clients.base import BaseClient
from app.infrastructure.clients.http import HTTPXClient
from app.infrastructure.services.calendar.base import CalendarService
from app.infrastructure.services.calendar.http import HTTPCalendarService
from app.infrastructure.services.user.base import UserService
from app.infrastructure.services.user.http import HttpUserService
from app.logic.bootstrap import Bootstrap
from app.logic.types.handlers import CommandHandlerMapping, EventHandlerMapping, UT
from app.settings.config import Settings


class HandlerProvider(Provider):
    """
    Here you have to link commands and command handlers for future inject in Bootstrap
    """

    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        return cast(
            CommandHandlerMapping,
            {
                
            }
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            EventHandlerMapping,
            {

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
                group_id=f"tasks-service-group",
                metadata_max_age_ms=30000,
            ),
        )


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            broker: BaseMessageBroker,
            user_service: UserService,
            calendar_service: CalendarService,
            uow: UT
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"broker": broker, "user_service": user_service, "calendar_service": calendar_service},
        )


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
            transport=transport,
            timeout=Timeout(settings.client.timeout)
        )

    @provide(scope=Scope.APP)
    async def get_http_client(self, client: AsyncClient) -> BaseClient:
        return HTTPXClient(client=client)

    @provide(scope=Scope.APP)
    async def get_user_client_service(self, client: BaseClient, settings: Settings) -> UserService:
        return HttpUserService(
            client=client, base_path=settings.client.user_endpoint_url
        )

    @provide(scope=Scope.APP)
    async def get_calendar_client_service(self, client: BaseClient, settings: Settings) -> CalendarService:
        return HTTPCalendarService(
            client=client, base_path=settings.client.calendar_endpoint_url
        )


container = make_async_container(
    DatabaseProvider(),
    HandlerProvider(),
    BrokerProvider(),
    AppProvider(),
    HTTPProvider(),
    context={
        Settings: Settings(),
    }
)
