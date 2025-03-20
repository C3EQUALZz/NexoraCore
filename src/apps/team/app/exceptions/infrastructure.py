from dataclasses import dataclass
from app.exceptions.base import BaseAppException
from abc import ABC
from http import HTTPStatus


@dataclass(eq=False)
class InfrastructureException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class ConvertingException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Converting exception in sqlalchemy typedecorator has occurred. {self.value}"


@dataclass(eq=False)
class TeamNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Couldn't find team {self.value}"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value


@dataclass(eq=False)
class AttributeException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"ATTRIBUTE_REQUIRED! {self.value} is required"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class TeamAlreadyExistsException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Provided team name already exists: {self.value}, please choose another name"

    @property
    def status(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class UserAlreadyExistsInTeamException(InfrastructureException):
    team_id: str
    user_id: str

    @property
    def message(self) -> str:
        return f"Person {self.user_id} already exists in team {self.team_id}"

    @property
    def status(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class UserDoesntExistsInThisTeamException(InfrastructureException):
    user_id: str
    team_id: str

    @property
    def message(self) -> str:
        return f"Person with oid: {self.user_id} doesn't exists in this team: {self.team_id}"


@dataclass(eq=False)
class EmptyJsonResponseException(InfrastructureException):
    @property
    def message(self) -> str:
        return f"Wrong request on users microservice, check availability"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class EmptyRoleFieldInJsonException(InfrastructureException):
    @property
    def message(self) -> str:
        return f"User doesn't have field 'role', please check the users microservice"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value
