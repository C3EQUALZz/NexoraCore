from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.user import UserEntity
from app.infrastructure.adapters.alchemy.mappers.user import UserMapper
from app.infrastructure.adapters.alchemy.orm import UserModel
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.users.base import UsersRepository


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):
    __mapper: UserMapper = UserMapper()

    @override
    async def add(self, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            insert(UserModel)
            .values(**await model.to_dict())
            .returning(UserModel)
        )
        return self.__mapper.map_to_domain_entity(result.scalar_one())

    @override
    async def get(self, oid: str) -> UserEntity | None:
        result: Result = await self._session.execute(
            select(UserModel).filter_by(oid=oid)
        )

        model: UserModel | None = result.scalar_one_or_none()

        return None if model is None else self.__mapper.map_to_domain_entity(model)


    @override
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            update(UserEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(UserEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(UserEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[UserEntity]:
        result: Result = await self._session.execute(select(UserEntity).offset(start).limit(limit))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, UserEntity)

        return trading_result_entities
