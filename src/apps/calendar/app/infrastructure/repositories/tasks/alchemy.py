from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.events.task import TaskEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.tasks.base import TasksRepository


class SQLAlchemyTasksRepository(SQLAlchemyAbstractRepository, TasksRepository):
    @override
    async def get_by_assignee_id(
            self,
            assignee_id: str
    ) -> list[TaskEntity]:
        raise NotImplementedError

    @override
    async def get_by_assignee_id_and_status(self, assignee_id: str, status: str) -> TaskEntity:
        raise NotImplementedError

    @override
    async def list_by_status(
            self,
            status: str,
            start: int | None = None,
            limit: int | None = None
    ) -> list[TaskEntity]:
        raise NotImplementedError

    @override
    async def add(self, model: TaskEntity) -> TaskEntity:
        result: Result = await self._session.execute(
            insert(TaskEntity).values(**await model.to_dict()).returning(TaskEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> TaskEntity | None:
        result: Result = await self._session.execute(
            select(TaskEntity).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        result: Result = await self._session.execute(
            update(TaskEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(TaskEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TaskEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[TaskEntity]:

        if not (start is None and limit is None):
            result: Result = await self._session.execute(select(TaskEntity).offset(start).limit(limit))
        else:
            result: Result = await self._session.execute(select(TaskEntity))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, TaskEntity)

        return trading_result_entities
