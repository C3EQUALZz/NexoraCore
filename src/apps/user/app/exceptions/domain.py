from abc import ABC
from dataclasses import dataclass
from http import HTTPStatus

from app.exceptions.base import ApplicationException


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


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
class EmptyPasswordException(DomainException):
    @property
    def message(self) -> str:
        return "Password is empty"


@dataclass(eq=False)
class InvalidPasswordLengthException(DomainException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is invalid: {self.length}"


@dataclass(eq=False)
class EmptyGenderException(DomainException):
    @property
    def message(self) -> str:
        return "Gender is empty. Please provide some data about the gender"


@dataclass(eq=False)
class RoleException(DomainException):
    @property
    def message(self) -> str:
        return "Role does not exist. Please choose admin or user"


@dataclass(eq=False)
class StatusException(DomainException):
    @property
    def message(self) -> str:
        return "Status can be only logged-in or logged-out"


@dataclass(eq=False)
class URLMalformedException(DomainException):
    @property
    def message(self) -> str:
        return "URL is malformed"


@dataclass(eq=False)
class PhoneNumberException(DomainException):
    @property
    def message(self) -> str:
        return "Phone number is invalid"


@dataclass(eq=False)
class UnExistingGenderException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Gender {self.value} does not exist, please choose male or female"
