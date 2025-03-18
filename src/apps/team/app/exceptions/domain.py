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
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"

    @property
    def status(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


@dataclass(eq=False)
class EmptyEmailException(DomainException):
    @property
    def message(self) -> str:
        return "Email is empty"


@dataclass(eq=False)
class InvalidEmailException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided email is invalid: {self.email}"


@dataclass(eq=False)
class EmptyNamePartException(DomainException):

    @property
    def message(self) -> str:
        return f"The provided name is empty, please check data"


@dataclass(eq=False)
class PartNameTooShortException(DomainException):
    part_of_name: str
    bound: str

    @property
    def message(self) -> str:
        return f"The provided name was too short: {self.part_of_name}. Please provide with length bigger than: {self.bound}"


@dataclass(eq=False)
class PartNameTooLongException(DomainException):
    part_of_name: str
    bound: str

    @property
    def message(self) -> str:
        return f"The provided name was too long: {self.part_of_name}. Please provide with length lower than: {self.bound}"


@dataclass(eq=False)
class InvalidPartNameException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"The provided value was invalid: {self.value}. Please write normal part of name"
