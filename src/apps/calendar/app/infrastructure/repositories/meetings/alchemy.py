from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.events.meeting import MeetingEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.meetings.base import MeetingsRepository


class SQLAlchemyMeetingsRepository(SQLAlchemyAbstractRepository, MeetingsRepository):

    @override
    async def add(self, model: MeetingEntity) -> MeetingEntity:
        result: Result = await self._session.execute(
            insert(MeetingEntity).values(**await model.to_dict()).returning(MeetingEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> MeetingEntity | None:
        result: Result = await self._session.execute(
            select(MeetingEntity).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: MeetingEntity) -> MeetingEntity:
        result: Result = await self._session.execute(
            update(MeetingEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(MeetingEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(MeetingEntity).filter_by(oid=oid))

    @override
    async def get_by_organizer_id(self, organizer_id: str) -> list[MeetingEntity]:
        raise NotImplementedError

    @override
    async def list_by_participant_id(
            self,
            participant_id: str,
            start: int | None = None,
            limit: int | None = None
    ) -> list[MeetingEntity]:
        raise NotImplementedError

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[MeetingEntity]:

        if not (start is None and limit is None):
            result: Result = await self._session.execute(select(MeetingEntity).offset(start).limit(limit))
        else:
            result: Result = await self._session.execute(select(MeetingEntity))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, MeetingEntity)

        return trading_result_entities
