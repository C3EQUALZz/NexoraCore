from dataclasses import dataclass
from app.exceptions.base import ApplicationException
from abc import ABC
from http import HTTPStatus


@dataclass(eq=False)
class InfrastructureException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Infrastructure exception has occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


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
class PersonAlreadyExistsInTeamException(InfrastructureException):
    team: str
    team_member: str

    @property
    def message(self) -> str:
        return f"Person {self.team_member} already exists in team {self.team}"

    @property
    def status(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class PersonDoesntExistsException(InfrastructureException):
    person_id: str
    team_id: str

    @property
    def message(self) -> str:
        return f"Person with oid: {self.person_id} doesn't exists in this team: {self.team_id}"

