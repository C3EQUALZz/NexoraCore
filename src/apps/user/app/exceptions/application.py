from http import HTTPStatus

from app.exceptions.base import BaseAppException
from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(BaseAppException):
    @property
    def message(self) -> str:
        return "Exception on application layer has been occurred"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class EmptyCredentialsException(ApplicationException):
    @property
    def message(self) -> str:
        return "Credentials for auth cannot be empty"

    @property
    def status(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


@dataclass(eq=False)
class ForbiddenTokenException(ApplicationException):
    @property
    def message(self) -> str:
        return "This token has been revoked. Please get a new token."

    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value


@dataclass(eq=False)
class AuthException(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return self.value

    @property
    def status(self) -> int:
        return HTTPStatus.FORBIDDEN.value
