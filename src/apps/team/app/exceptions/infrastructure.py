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
        return f"Couldn't find user {self.value}"

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
        return f"TEAM ALREADY EXISTS! {self.value}"

    @property
    def status(self) -> int:
        return HTTPStatus.CONFLICT.value
