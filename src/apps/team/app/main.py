from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI

from app.application.api.v1.team_members.handlers import router as team_members_router
from app.application.api.v1.teams.handlers import router as teams_router
from app.logic.container import container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    yield

    await app.state.dishka_container.close()


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
