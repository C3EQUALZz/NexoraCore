import builtins
from typing import override, Mapping, Any

from motor.motor_asyncio import AsyncIOMotorCursor

from app.domain.entities.team_members import TeamMemberEntity
from app.infrastructure.repositories.base import MotorAbstractRepository
from app.infrastructure.repositories.team_members.base import TeamMembersRepository


class MotorTeamMembersRepository(MotorAbstractRepository, TeamMembersRepository):
    @override
    async def get_by_user_id(self, team_id: str, user_id: str) -> TeamMemberEntity | None:
        team_member = await self._collection.find_one(filter={"team_id":team_id, "user_id": user_id})
        return TeamMemberEntity.from_document(team_member) if team_member else None

    @override
    async def add(self, model: TeamMemberEntity) -> TeamMemberEntity:
        await self._collection.insert_one(await model.to_dict())
        return model

    @override
    async def get(self, oid: str) -> TeamMemberEntity | None:
        team_member = await self._collection.find_one(filter={"oid": oid})
        return TeamMemberEntity.from_document(team_member) if team_member else None

    @override
    async def update(self, oid: str, model: TeamMemberEntity) -> TeamMemberEntity:
        update_data = await model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def is_exists_in_team(self, user_id: str, team_id: str) -> bool:
        team_member = await self._collection.find_one(filter={"user_id": user_id, "team_id": team_id})
        return bool(team_member)

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        team_members: list[Mapping[str, Any]] = await cursor.to_list(length=limit)
        return [TeamMemberEntity.from_document(user) for user in team_members]

    @override
    async def delete(self, oid: str) -> None:
        await self._collection.find_one_and_delete(filter={"oid": oid})

    @override
    async def get_all_members_in_team(
            self,
            team_id: str,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TeamMemberEntity]:
        cursor: AsyncIOMotorCursor[Any] = self._collection.find(filter={"team_id": team_id}).skip(start).limit(limit)
        team_members: list[Mapping[str, Any]] = await cursor.to_list(length=limit)
        return [TeamMemberEntity.from_document(user) for user in team_members]

    @override
    async def delete_by_user_id_and_team_id(self, user_id: str, team_id: str) -> None:
        await self._collection.find_one_and_delete(filter={"user_id": user_id, "team_id": team_id})
