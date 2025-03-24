from app.domain.entities.events.task import TaskEntity
from app.domain.entities.user import UserEntity
from app.infrastructure.services.tasks import TasksService
from app.infrastructure.services.user import UserService
from app.logic.commands.tasks import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand
from app.logic.handlers.tasks.base import TasksCommandHandler


class CreateTaskCommandHandler(TasksCommandHandler[CreateTaskCommand]):
    async def __call__(self, command: CreateTaskCommand) -> TaskEntity:
        task_service: TasksService = TasksService(self._uow)
        user_service: UserService = UserService(self._uow)

        assignee: UserEntity = await user_service.get_by_id(command.assignee_id)
        created_by: UserEntity = await user_service.get_by_id(command.created_by_id)

        new_task: TaskEntity = TaskEntity(
            assignee=assignee,
            title=command.title,
            description=command.description,
            start_time=command.start_time,
            end_time=command.end_time,
            created_by=created_by,
        )

        return await task_service.add(new_task)


class UpdateTaskCommandHandler(TasksCommandHandler[UpdateTaskCommand]):
    async def __call__(self, command: UpdateTaskCommand) -> TaskEntity:
        task_service: TasksService = TasksService(self._uow)
        user_service: UserService = UserService(self._uow)

        assignee: UserEntity = await user_service.get_by_id(command.assignee_id)
        created_by: UserEntity = await user_service.get_by_id(command.created_by_id)

        updated_task: TaskEntity = TaskEntity(
            oid=command.oid,
            title=command.title,
            description=command.description,
            start_time=command.start_time,
            end_time=command.end_time,
            created_by=created_by,
            assignee=assignee,
            status=command.status,
        )

        return await task_service.update(command.oid, updated_task)


class DeleteTaskCommandHandler(TasksCommandHandler[DeleteTaskCommand]):
    async def __call__(self, command: DeleteTaskCommand) -> None:
        task_service: TasksService = TasksService(self._uow)
        return await task_service.delete(command.oid)
