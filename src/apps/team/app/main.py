from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import clear_mappers

from app.application.api.v1.teams.handlers import router as teams_router
from app.application.api.v1.team_members.handlers import router as team_members_router
from app.infrastructure.adapters.alchemy.orm import start_mappers, metadata
from app.logic.container import container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    engine: AsyncEngine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    yield

    await app.state.dishka_container.close()
    clear_mappers()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Microservice backend for teams service",
        description="Backend API written with FastAPI for teams service",
        debug=True,
        root_path="/api/v1/teams",
        lifespan=lifespan
    )

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(teams_router)
    app.include_router(team_members_router)

    return app
