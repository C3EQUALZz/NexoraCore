from abc import abstractmethod
from typing import TypeVar, Protocol

DT = TypeVar('DT', bound=object)  # Domain Entity Type
PT = TypeVar('PT', bound=object)  # Persistence Entity Type


class BaseModelMapper(Protocol[DT, PT]):
    @staticmethod
    @abstractmethod
    def map_to_domain_entity(model: PT) -> DT:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def map_to_persistence_entity(entity: DT) -> PT:
        raise NotImplementedError
