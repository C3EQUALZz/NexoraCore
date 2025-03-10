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
