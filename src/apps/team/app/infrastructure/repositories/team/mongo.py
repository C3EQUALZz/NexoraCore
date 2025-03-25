from motor.motor_asyncio import AsyncIOMotorCursor

from app.infrastructure.repositories.base import MotorAbstractRepository
from app.infrastructure.repositories.team.base import TeamsRepository
from typing import override, Any, Mapping
from app.domain.entities.team import TeamEntity


class MotorTeamsRepository(TeamsRepository, MotorAbstractRepository):
    @override
    async def get_by_team_name(self, name: str) -> TeamEntity | None:
        user = await self._collection.find_one(filter={"name": name})
        return TeamEntity.from_document(user) if user else None

    @override
    async def add(self, model: TeamEntity) -> TeamEntity:
        await self._collection.insert_one(await model.to_dict())
        return model

    @override
    async def get(self, oid: str) -> TeamEntity | None:
        team = await self._collection.find_one(filter={"oid": oid})
        return TeamEntity.from_document(team) if team else None

    @override
    async def update(self, oid: str, model: TeamEntity) -> TeamEntity:
        update_data = await model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def delete(self, oid: str) -> None:
        await self._collection.find_one_and_delete(filter={"oid": oid})

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamEntity]:
        cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        scores: list[Mapping[str, Any]] = await cursor.to_list(length=limit)
        return [TeamEntity.from_document(user) for user in scores]
