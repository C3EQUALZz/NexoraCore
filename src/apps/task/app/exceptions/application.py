from abc import (
    ABC,
)
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import BaseAppException


@dataclass(eq=False)
class ApplicationException(BaseAppException, ABC):
    @property
    def message(self) -> str:
        return "An error on application layer has been occured"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

    @property
    def headers(self) -> dict[str, str] | None:
        return None

