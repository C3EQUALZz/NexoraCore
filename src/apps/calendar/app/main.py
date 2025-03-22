from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.adapters.alchemy.orm import Base
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import container
from app.settings.config import get_settings, Settings
from app.settings.logger.config import setup_logging
from app.application.api.v1.tasks.handlers import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings: Settings = get_settings()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    await broker.start()

    engine: AsyncEngine = create_async_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await broker.close()
    await app.state.dishka_container.close()


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

    return app
