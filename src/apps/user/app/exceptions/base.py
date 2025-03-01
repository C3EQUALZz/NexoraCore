from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception, ABC):
    @property
    def message(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.message