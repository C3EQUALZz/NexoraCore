from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundException
from app.infrastructure.uow.events.base import EventsUnitOfWork


class UserService:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            new_user: UserEntity = await uow.users.add(user)
            await uow.commit()
            return new_user

    async def get_by_id(self, oid: str) -> UserEntity:
        async with self._uow as uow:
            user: UserEntity | None = await uow.users.get(oid=oid)

            if not user:
                raise UserNotFoundException(str(oid))

            return user

    async def update(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            updated_user = await uow.users.update(oid=user.oid, model=user)
            await uow.commit()
            return updated_user

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            user: UserEntity | None = await uow.users.get(oid=oid)

            if not user:
                raise UserNotFoundException(str(oid))

            await uow.users.delete(oid)
            await uow.commit()

    async def get_all(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        async with self._uow as uow:
            return await uow.users.list(start=start, limit=limit)
