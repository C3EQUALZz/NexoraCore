from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


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
class UserNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"User with oid: {self.value} not found in microservice users"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value


@dataclass(eq=False)
class UserServiceException(InfrastructureException):

    @property
    def message(self) -> str:
        return "Failed to fetch user from user microservice"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class NoSuchFieldException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"No such field: {self.value} from response from user microservice"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class ClientHTTPException(InfrastructureException):
    message: str
    url: str

    @property
    def message(self) -> str:
        return f"Bad HTTP status! message: {self.message}, url: {self.url}"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class ClientConnectionException(InfrastructureException):
    message: str
    url: str

    @property
    def message(self) -> str:
        return f"Connection error! message: {self.message}, url: {self.url}"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class UserNotFoundException(InfrastructureException):
    value: str

    @property
    def message(self) -> str:
        return f"User with oid: {self.value} not found in microservice users"

    @property
    def status(self) -> int:
        return HTTPStatus.NOT_FOUND.value


@dataclass(eq=False)
class UserServiceUnAvailableException(InfrastructureException):

    @property
    def message(self) -> str:
        return "User microservice is unavailable"

    @property
    def status(self) -> int:
        return HTTPStatus.SERVICE_UNAVAILABLE.value


@dataclass(eq=False)
class CalendarServiceUnAvailableException(InfrastructureException):
    @property
    def message(self) -> str:
        return "Calendar microservice is unavailable"

    @property
    def status(self) -> int:
        return HTTPStatus.SERVICE_UNAVAILABLE.value
