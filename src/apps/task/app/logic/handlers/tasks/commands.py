from app.domain.entities.task import TaskEntity
from app.domain.entities.user import UserEntity
from app.domain.values.task import Title, Description
from app.infrastructure.services.task import TasksService
from app.logic.commands.tasks import CreateTaskCommand, UpdateTaskCommand
from app.logic.events.tasks import TaskCreatedEvent
from app.logic.handlers.tasks.base import TasksCommandHandler


class CreateTaskCommandHandler(TasksCommandHandler[CreateTaskCommand]):
    async def __call__(self, command: CreateTaskCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)

            assigned_to: UserEntity = await self._client_service.get_user(command.assigned_to)
            created_by: UserEntity = await self._client_service.get_user(command.created_by)

            new_task: TaskEntity = TaskEntity(
                title=Title(command.title),
                description=Description(command.description),
                assigned_to=assigned_to,
                created_by=created_by,
                due_datetime=command.due_datetime,
            )

            added_task: TaskEntity = await task_service.add(new_task)

            await uow.add_event(
                TaskCreatedEvent(
                    task_id=added_task.oid,
                    email_assigned_to=assigned_to.email.as_generic_type()
                )
            )

            return added_task


class UpdateTaskCommandHandler(TasksCommandHandler[UpdateTaskCommand]):
    async def __call__(self, command: UpdateTaskCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)
