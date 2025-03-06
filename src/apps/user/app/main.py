from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import clear_mappers

from app.application.api.v1.users.handlers import router as user_router
from app.application.utils.admin_setup import setup_admin
from app.infrastructure.adapters.alchemy.metadata import metadata
from app.infrastructure.adapters.alchemy.orm import start_mappers
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.container import container
from app.settings.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    engine: AsyncEngine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    await setup_admin(await container.get(UsersUnitOfWork), await container.get(Settings))

    yield

    await app.state.dishka_container.close()
    clear_mappers()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Microservice backend for user service",
        description="Backend API written with FastAPI for user service",
        root_path="/api/user-service",
        debug=True,
        lifespan=lifespan,
    )

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(user_router)

    return app