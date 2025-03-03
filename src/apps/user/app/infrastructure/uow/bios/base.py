from abc import ABC

from app.infrastructure.repositories.bios.base import BiosRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class BiosUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with bio information of users, that is used by service layer of bios module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    bios: BiosRepository