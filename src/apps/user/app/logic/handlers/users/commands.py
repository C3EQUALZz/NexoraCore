from app.exceptions.infrastructure import UserNotFoundException
from app.exceptions.logic import UserAlreadyExistsException, InvalidPasswordException
from app.infrastructure.services.users import UsersService
from app.infrastructure.utils.security import hash_password, validate_password
from app.logic.handlers.users.base import UsersCommandHandler
from app.logic.commands.users import CreateUserCommand, VerifyUserCredentialsCommand, UpdateUserCommand
from app.domain.entities.user import UserEntity
from app.domain.values.user import Password


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if await user_service.check_existence(name=command.name, email=command.email):
            raise UserAlreadyExistsException(command.email)

        new_user: UserEntity = UserEntity(**await command.to_dict())
        new_user.password = Password(hash_password(command.password))

        return await user_service.add(new_user)


class UpdateUserCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if not await user_service.check_existence(oid=command.oid):
            raise UserNotFoundException(command.oid)

        user: UserEntity = await user_service.get_by_id(command.oid)

        updated_user = UserEntity(**await command.to_dict())
        updated_user.oid = user.oid

        return await user_service.update(updated_user)


class VerifyUserCredentialsCommandHandler(UsersCommandHandler[VerifyUserCredentialsCommand]):
    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserEntity:
        """
        Checks, if provided by user credentials are valid.
        """

        users_service: UsersService = UsersService(uow=self._uow)

        user: UserEntity
        if await users_service.check_existence(email=command.email):
            user = await users_service.get_by_email(email=command.email)
        else:
            raise UserNotFoundException(command.email)

        if not validate_password(password=command.password, hashed_password=user.password.as_generic_type()):
            raise InvalidPasswordException

        return user
