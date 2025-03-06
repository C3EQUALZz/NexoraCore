from typing import override, Sequence, Any

from sqlalchemy import Result, delete, Row, RowMapping, select, update, insert

from app.domain.entities.team import Team
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.team.base import TeamsRepository


class SQLAlchemyTeamsRepository(SQLAlchemyAbstractRepository, TeamsRepository):
    @override
    async def get_by_team_name(self, name: str) -> Team | None:
        result: Result = await self._session.execute(
            select(Team).filter_by(name=name)
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: Team) -> Team:
        result: Result = await self._session.execute(
            insert(Team).values(**await model.to_dict()).returning(Team)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> Team | None:
        result: Result = await self._session.execute(
            select(Team).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: Team) -> Team:
        result: Result = await self._session.execute(
            update(Team)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(Team)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(Team).filter_by(oid=oid))

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[Team]:
        result: Result = await self._session.execute(select(Team).offset(start).limit(limit))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, Team)

        return trading_result_entities
