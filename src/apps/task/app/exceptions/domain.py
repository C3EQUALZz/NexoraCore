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
class IncorrectAssessmentException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Incorrect assessment: {self.value}. It must be between 1 and 10"


@dataclass(eq=False)
class IncorrectCriteriaException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Incorrect criteria: {self.value}. Value can be only 'quality', 'completeness', 'timing'"


@dataclass(eq=False)
class EmptyTaskTitleException(DomainException):

    @property
    def message(self) -> str:
        return "Task title is empty. Please provide some info"


@dataclass(eq=False)
class EmtpyTaskDescriptionException(DomainException):

    @property
    def message(self) -> str:
        return "Task description is empty. Please provide some info"


@dataclass(eq=False)
class EmptyTaskStatusException(DomainException):
    @property
    def message(self) -> str:
        return "Task status is empty. Please provide some info"


@dataclass(eq=False)
class InvalidTaskStatusException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Task status is invalid: {self.value}. Task status can be only: 'open', 'in_progress', 'completed'"


@dataclass(eq=False)
class ObsceneTextException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"{self.text[:30]} is an obscene text"


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
class RoleException(DomainException):
    @property
    def message(self) -> str:
        return "Role does not exist. Please choose admin or staffer, manager"
