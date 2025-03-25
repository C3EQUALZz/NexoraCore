from app.domain.values.base import BaseValueObject
from dataclasses import dataclass
from typing import override

from app.exceptions.domain import EmptyTaskTitleException, EmtpyTaskDescriptionException, EmptyTaskStatusException, \
    InvalidTaskStatusException


@dataclass
class Title(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value or self.value.isspace():
            raise EmptyTaskTitleException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class Description(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value or self.value.isspace():
            raise EmtpyTaskDescriptionException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class TaskStatus(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value or self.value.isspace():
            raise EmptyTaskStatusException()

        if self.value not in ("open", "in_progress", "completed"):
            raise InvalidTaskStatusException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
