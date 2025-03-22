import logging
from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert
from sqlalchemy.orm import joinedload

from app.domain.entities.events.task import TaskEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.tasks.base import TasksRepository

logger = logging.getLogger(__name__)


class SQLAlchemyTasksRepository(SQLAlchemyAbstractRepository, TasksRepository):
    @override
    async def get_by_assignee_id(
            self,
            assignee_id: str
    ) -> list[TaskEntity]:
        result: Result = await self._session.execute(select(TaskEntity).filter_by(assignee_id=assignee_id))
        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, TaskEntity)

        return entities

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

        data = await model.to_dict()

        data['assignee_id'] = data.pop('assignee').get('oid')
        data['created_by_id'] = data.pop('created_by').get('oid')

        result: Result = await self._session.execute(
            insert(TaskEntity)
            .values(**data)
            .returning(TaskEntity.oid)
        )

        task_id: str = result.scalar_one()

        result: Result = await self._session.execute((
            select(TaskEntity)
            .where(TaskEntity.oid == task_id) # type: ignore
            .options(
                joinedload(TaskEntity.assignee), # type: ignore
                joinedload(TaskEntity.created_by) # type: ignore
            )
        ))

        return result.scalar_one()

    @override
    async def get(self, oid: str) -> TaskEntity | None:
        result: Result = await self._session.execute(
            select(TaskEntity)
            .filter_by(oid=oid)
            .options(joinedload(TaskEntity.created_by), joinedload(TaskEntity.assignee)) # type: ignore
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        ...

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TaskEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[TaskEntity]:
        ...
