from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.calendar import CalendarEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.calendar.base import CalendarsRepository


class SQLAlchemyCalendarsRepository(SQLAlchemyAbstractRepository, CalendarsRepository):

    @override
    async def get_by_owner_id(self, owner_id: str) -> CalendarEntity | None:
        raise NotImplementedError

    @override
    async def add(self, model: CalendarEntity) -> CalendarEntity:
        result: Result = await self._session.execute(
            insert(CalendarEntity).values(**await model.to_dict()).returning(CalendarEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> CalendarEntity | None:
        result: Result = await self._session.execute(
            select(CalendarEntity).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: CalendarEntity) -> CalendarEntity:
        result: Result = await self._session.execute(
            update(CalendarEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(CalendarEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(CalendarEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[CalendarEntity]:

        if not (start is None and limit is None):
            result: Result = await self._session.execute(select(CalendarEntity).offset(start).limit(limit))
        else:
            result: Result = await self._session.execute(select(CalendarEntity))

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, CalendarEntity)

        return entities
