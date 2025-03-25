from datetime import datetime
from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update, and_, exists
from sqlalchemy.orm import joinedload

from app.domain.entities.events.task import TaskEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.tasks.base import TasksRepository


class SQLAlchemyTasksRepository(SQLAlchemyAbstractRepository, TasksRepository):
    @override
    async def get_by_assignee_id(
            self,
            assignee_id: str
    ) -> list[TaskEntity]:

        result: Result = await self._session.execute(
            select(TaskEntity)
            .filter_by(assignee_id=assignee_id)
            .options(
                joinedload(TaskEntity.created_by),  # type: ignore
                joinedload(TaskEntity.assignee)  # type: ignore
            )
        )

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, TaskEntity)

        return entities

    @override
    async def get_by_assignee_id_and_status(self, assignee_id: str, status: str) -> list[TaskEntity]:
        result: Result = await self._session.execute(
            select(TaskEntity)
            .filter_by(assignee_id=assignee_id, status=status)
            .options(
                joinedload(TaskEntity.created_by),  # type: ignore
                joinedload(TaskEntity.assignee)  # type: ignore
            )
        )

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, TaskEntity)

        return entities

    @override
    async def list_by_status(
            self,
            status: str,
            start: int | None = None,
            limit: int | None = None
    ) -> list[TaskEntity]:
        if start is not None and limit is not None:
            result: Result = await self._session.execute(
                select(TaskEntity)
                .filter_by(status=status)
                .options(
                    joinedload(TaskEntity.created_by),  # type: ignore
                    joinedload(TaskEntity.assignee)  # type: ignore
                )
                .offset(start)
                .limit(limit)
            )
        else:
            result: Result = await self._session.execute(
                select(TaskEntity)
                .filter_by(status=status)
                .options(
                    joinedload(TaskEntity.created_by),  # type: ignore
                    joinedload(TaskEntity.assignee)  # type: ignore
                )
            )

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, TaskEntity)

        return entities

    @override
    async def add(self, model: TaskEntity) -> TaskEntity:
        result: Result = await self._session.execute(
            insert(TaskEntity)
            .values(**await model.to_dict())
            .returning(TaskEntity.oid)
        )

        task_id: str = result.scalar_one()

        return await self.get(task_id)

    @override
    async def get(self, oid: str) -> TaskEntity | None:
        result: Result = await self._session.execute(
            select(TaskEntity)
            .filter_by(oid=oid)
            .options(
                joinedload(TaskEntity.created_by),  # type: ignore
                joinedload(TaskEntity.assignee)  # type: ignore
            )
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        result: Result = await self._session.execute(
            update(TaskEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict())
            .returning(TaskEntity.oid)
        )

        task_id: str = result.scalar_one()

        return await self.get(task_id)

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TaskEntity).filter_by(oid=oid))

    @override
    async def list(
            self,
            start: int | None = None,
            limit: int | None = None
    ) -> list[TaskEntity]:
        if start is None and limit is None:
            result: Result = await self._session.execute(
                select(TaskEntity)
                .options(
                    joinedload(TaskEntity.created_by),  # type: ignore
                    joinedload(TaskEntity.assignee)  # type: ignore
                )
            )

        else:
            result: Result = await self._session.execute(
                select(TaskEntity)
                .options(
                    joinedload(TaskEntity.created_by),  # type: ignore
                    joinedload(TaskEntity.assignee)  # type: ignore
                )
                .offset(start)
                .limit(limit)
            )

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, TaskEntity)

        return entities

    @override
    async def is_user_available_for_this_time(
            self,
            assignee_id: str,
            start_time: datetime,
            end_time: datetime
    ) -> bool:
        # Условия фильтрации
        result: Result = await self._session.execute(exists().where(
            and_(
                TaskEntity.assignee_id == assignee_id, # type: ignore
                TaskEntity.status.in_(["pending", "in_progress"]), # type: ignore
                and_(
                    TaskEntity.start_time < end_time,
                    TaskEntity.end_time > start_time
                )
            )
        ).select())

        return not result.scalar()



