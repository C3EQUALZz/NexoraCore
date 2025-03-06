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
