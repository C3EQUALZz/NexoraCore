from app.domain.values.base import BaseValueObject
from dataclasses import dataclass
from typing import override


@dataclass
class TeamName(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        ...

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class TeamDescription(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        ...

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
