from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.team_members import TeamMemberEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.team_members.base import TeamMembersRepository


class SQLAlchemyTeamMembersRepository(SQLAlchemyAbstractRepository, TeamMembersRepository):
    @override
    async def get_by_user_id(self, user_id: str) -> TeamMemberEntity | None:
        result: Result = await self._session.execute(
            select(TeamMemberEntity).filter_by(user_id=user_id)
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: TeamMemberEntity) -> TeamMemberEntity:
        result: Result = await self._session.execute(
            insert(TeamMemberEntity).values(**await model.to_dict()).returning(TeamMemberEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> TeamMemberEntity | None:
        result: Result = await self._session.execute(
            select(TeamMemberEntity).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: TeamMemberEntity) -> TeamMemberEntity:
        result: Result = await self._session.execute(
            update(TeamMemberEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(TeamMemberEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TeamMemberEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        result: Result = await self._session.execute(select(TeamMemberEntity).offset(start).limit(limit))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, TeamMemberEntity)

        return trading_result_entities
