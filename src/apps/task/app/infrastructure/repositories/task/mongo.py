from motor.motor_asyncio import AsyncIOMotorCursor

from app.infrastructure.repositories.base import MotorAbstractRepository
from app.infrastructure.repositories.task.base import TasksRepository
from typing import override, Any, Mapping
from app.domain.entities.task import TaskEntity


class MotorTasksRepository(TasksRepository, MotorAbstractRepository):
    @override
    async def get_by_title_and_description(self, title: str, description: str) -> TaskEntity | None:
        task = await self._collection.find_one(filter={"title": title, "description": description})
        return TaskEntity.from_document(task)

    @override
    async def get_by_assigned_to_and_created_by(self, assigned_to: str, created_by: str) -> TaskEntity | None:
        task = await self._collection.find_one(filter={"assigned_to": assigned_to, "created_by": created_by})
        return TaskEntity.from_document(task)

    @override
    async def add(self, model: TaskEntity) -> TaskEntity:
        await self._collection.insert_one(await model.to_dict())
        return model

    @override
    async def get(self, oid: str) -> TaskEntity | None:
        team = await self._collection.find_one(filter={"oid": oid})
        return TaskEntity.from_document(team) if team else None

    @override
    async def update(self, oid: str, model: TaskEntity) -> TaskEntity:
        update_data = await model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def delete(self, oid: str) -> None:
        await self._collection.find_one_and_delete(filter={"oid": oid})

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[TaskEntity]:
        cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        teams: list[Mapping[str, Any]] = await cursor.to_list(length=limit)
        return [TaskEntity.from_document(user) for user in teams]
