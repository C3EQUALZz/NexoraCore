from app.domain.entities.events.task import TaskEntity
from app.infrastructure.adapters.alchemy.mappers.base import BaseModelMapper
from app.infrastructure.adapters.alchemy.mappers.user import UserMapper
from app.infrastructure.adapters.alchemy.orm import TaskModel


class TaskMapper(BaseModelMapper[TaskEntity, TaskModel]):
    @staticmethod
    def map_to_domain_entity(model: TaskModel) -> TaskEntity:
        return TaskEntity(
            oid=model.oid,
            title=model.title,
            description=model.description,
            start_time=model.start_time,
            end_time=model.end_time,
            assignee=UserMapper.map_to_domain_entity(model.assignee),
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=UserMapper.map_to_domain_entity(model.created_by)
        )

    @staticmethod
    def map_to_persistence_entity(entity: TaskEntity) -> TaskModel:
        return TaskModel(
            oid=entity.oid,
            title=entity.title,
            description=entity.description,
            start_time=entity.start_time,
            end_time=entity.end_time,
            assignee_id=UserMapper.map_to_persistence_entity(entity.assignee).oid,
            created_by_id=UserMapper.map_to_persistence_entity(entity.created_by).oid,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
