from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class DomainException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None


@dataclass(eq=False)
class RoleException(DomainException):
    @property
    def message(self) -> str:
        return "Role does not exist. Please choose admin or staffer, manager"
