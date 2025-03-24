from dataclasses import dataclass
from app.domain.values.base import BaseValueObject
from typing import override

from app.exceptions.domain import RoleException


@dataclass
class Role(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("admin", "staffer", "manager"):
            raise RoleException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
