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
