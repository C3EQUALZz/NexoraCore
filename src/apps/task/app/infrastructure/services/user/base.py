from abc import abstractmethod, ABC

from app.domain.entities.user import UserEntity


class UserService(ABC):
    """Client for user microservice"""

    @abstractmethod
    async def get_user(self, user_oid: str) -> UserEntity:
        """Get user by id, if it exists"""
        raise NotImplementedError
