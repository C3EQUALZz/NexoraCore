from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI


from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import container
from app.settings.logger.config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    await broker.start()

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

    return app
