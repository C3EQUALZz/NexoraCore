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
class TaskNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"Couldn't find team {self.value}"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value

@dataclass(eq=False)
class MeetingNotFoundException(InfrastructureException):
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

