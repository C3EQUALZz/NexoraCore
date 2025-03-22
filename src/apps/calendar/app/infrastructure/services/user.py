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