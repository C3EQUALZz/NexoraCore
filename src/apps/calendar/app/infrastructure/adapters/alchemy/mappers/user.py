from app.domain.entities.user import UserEntity
from app.infrastructure.adapters.alchemy.mappers.base import BaseModelMapper
from app.infrastructure.adapters.alchemy.orm import UserModel


class UserMapper(BaseModelMapper[UserEntity, UserModel]):
    @staticmethod
    def map_to_domain_entity(model: UserModel) -> UserEntity:
        return UserEntity(oid=str(model.oid))

    @staticmethod
    def map_to_persistence_entity(entity: UserEntity) -> UserModel:
        return UserModel(oid=entity.oid)
