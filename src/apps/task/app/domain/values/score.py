from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import IncorrectAssessmentException, IncorrectCriteriaException


@dataclass
class ScoreValue(BaseValueObject[int]):
    value: int

    @override
    def validate(self) -> None:
        if not 1 < self.value < 10:
            raise IncorrectAssessmentException(str(self.value))

    @override
    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass
class Criteria(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("quality", "completeness", "timing"):
            raise IncorrectCriteriaException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
