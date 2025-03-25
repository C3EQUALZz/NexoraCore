import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import clear_mappers

from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.adapters.alchemy.orm import metadata, start_mappers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.consumers.manager import ConsumerManager
from app.logic.container import container
from app.settings.config import get_settings, Settings
from app.settings.logger.config import setup_logging
from app.application.api.v1.tasks.handlers import router as tasks_router
from app.application.api.v1.meetings.handlers import router as meetings_router
from app.application.api.v1.user.handlers import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings: Settings = get_settings()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    manager: ConsumerManager = await container.get(ConsumerManager)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    await broker.start()
    asyncio.create_task(manager.start_all())

    engine: AsyncEngine = create_async_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    yield

    await manager.stop_all()
    await broker.stop_consuming_all()
    await broker.close()

    await app.state.dishka_container.close()
    clear_mappers()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Microservice backend for calendar service",
        description="Backend API written with FastAPI for calendar service",
        debug=True,
        root_path="/api/v1/calendar",
        lifespan=lifespan
    )

    setup_logging()
    register_exception_handlers(app)

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(tasks_router)
    app.include_router(meetings_router)
    app.include_router(users_router)

    return app
