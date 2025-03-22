from typing import override

from sqlalchemy import Result, select, delete, update
from sqlalchemy.orm import joinedload

from app.domain.entities.events.task import TaskEntity
from app.infrastructure.adapters.alchemy.mappers.task import TaskMapper
from app.infrastructure.adapters.alchemy.orm import TaskModel
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.tasks.base import TasksRepository


class SQLAlchemyTasksRepository(SQLAlchemyAbstractRepository, TasksRepository):
    __mapper: TaskMapper = TaskMapper()

    @override
    async def get_by_assignee_id(
            self,
            assignee_id: str
    ) -> list[TaskEntity]:

        result: Result = await self._session.execute(
            select(TaskModel)
            .filter_by(assignee_id=assignee_id)
        )

        entities: list[TaskEntity] = [
            self.__mapper.map_to_domain_entity(x)
            for x in result.scalars().all()
        ]

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
        # Конвертируем доменную сущность в модель SQLAlchemy
        task_model = self.__mapper.map_to_persistence_entity(model)

        # Добавляем модель в сессию
        self._session.add(task_model)

        # Выполняем flush, чтобы получить сгенерированные значения (например, ID)
        await self._session.flush()

        # Явно обновляем модель, загружая связи
        await self._session.refresh(
            task_model,
            attribute_names=['assignee', 'created_by']
        )

        # Конвертируем обратно в доменную сущность
        return self.__mapper.map_to_domain_entity(task_model)

    @override
    async def get(self, oid: str) -> TaskEntity | None:
        result: Result = await self._session.execute(
            select(TaskModel)
            .filter_by(oid=oid)
            .options(joinedload(TaskModel.created_by), joinedload(TaskModel.assignee))
        )
        model: TaskModel | None = result.scalar_one_or_none()
        return None if model is None else self.__mapper.map_to_domain_entity(model)

    @override
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        result = await self._session.execute(
            update(TaskModel)
            .where(TaskModel.oid == oid)
            .values(**await model.to_dict(exclude={"created_at", "oid"}))
            .returning(TaskModel)
        )
        return self.__mapper.map_to_domain_entity(result.scalar_one())

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TaskModel).filter_by(oid=oid))

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[TaskEntity]:
        if not (start is None and limit is None):
            result: Result = await self._session.execute(
                select(TaskModel)
                .offset(start)
                .limit(limit)
            )
        else:
            result: Result = await self._session.execute(select(TaskModel))

        entities: list[TaskEntity] = [
            self.__mapper.map_to_domain_entity(x)
            for x in result.scalars().all()
        ]

        return entities
