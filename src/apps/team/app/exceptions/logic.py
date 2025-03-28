from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class LogicException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "An logic error has occurred"

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class MessageBusMessageException(LogicException):
    @property
    def message(self) -> str:
        return "Message bus message should be eiter of Event type, or Command type"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class UserDoesntExistException(LogicException):
    value: str

    @property
    def message(self) -> str:
        return f"User with oid: {self.value} doesn't exist, please peek a real id"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value
