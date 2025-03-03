from abc import ABC

from app.infrastructure.repositories.user.base import UserRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class UserUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with users, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    products_market: UserRepository
