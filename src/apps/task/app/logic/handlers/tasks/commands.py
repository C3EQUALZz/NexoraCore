from app.domain.entities.task import TaskEntity
from app.domain.entities.user import UserEntity
from app.domain.values.shared import Comment
from app.domain.values.task import Title, Description, TaskStatus
from app.exceptions.logic import UserUnAvailableNowException
from app.infrastructure.services.task import TasksService
from app.logic.commands.tasks import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand, UpdateTaskStatusCommand, \
    CreateNewCommentForTaskCommand
from app.logic.events.tasks import TaskCreatedEvent, TaskUpdatedEvent, TaskDeletedEvent
from app.logic.handlers.tasks.base import TasksCommandHandler


class CreateTaskCommandHandler(TasksCommandHandler[CreateTaskCommand]):
    async def __call__(self, command: CreateTaskCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)

            if not await self._calendar_service.is_user_is_available_for_period(
                user_oid=command.assigned_to,
                start_time=command.start_datetime,
                end_time=command.due_datetime
            ):
                raise UserUnAvailableNowException


            assigned_to: UserEntity = await self._client_service.get_user(command.assigned_to)
            created_by: UserEntity = await self._client_service.get_user(command.created_by)

            new_task: TaskEntity = TaskEntity(
                title=Title(command.title),
                description=Description(command.description),
                assigned_to=assigned_to,
                created_by=created_by,
                due_datetime=command.due_datetime,
                start_datetime=command.start_datetime
            )

            added_task: TaskEntity = await task_service.add(new_task)

            await uow.add_event(
                TaskCreatedEvent(
                    task_id=added_task.oid,
                    email_assigned_to=assigned_to.email.as_generic_type(),
                    start_datetime=added_task.start_datetime,
                    end_datetime=added_task.due_datetime
                )
            )

            await uow.commit()

            return added_task


class UpdateTaskCommandHandler(TasksCommandHandler[UpdateTaskCommand]):
    async def __call__(self, command: UpdateTaskCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)

            if not await self._calendar_service.is_user_is_available_for_period(
                user_oid=command.assigned_to,
                start_time=command.start_datetime,
                end_time=command.due_datetime
            ):
                raise UserUnAvailableNowException

            assigned_to: UserEntity = await self._client_service.get_user(command.assigned_to)
            created_by: UserEntity = await self._client_service.get_user(command.created_by)

            new_entity: TaskEntity = TaskEntity(
                oid=command.oid,
                title=Title(command.title),
                description=Description(command.description),
                due_datetime=command.due_datetime,
                assigned_to=assigned_to,
                created_by=created_by,
                start_datetime=command.start_datetime,
            )

            updated_task: TaskEntity = await task_service.update(oid=command.oid, model=new_entity)

            await uow.add_event(
                TaskUpdatedEvent(
                    task_id=updated_task.oid,
                    email_assigned_to=assigned_to.email.as_generic_type(),
                    start_datetime=updated_task.start_datetime,
                    end_datetime=updated_task.due_datetime,
                    status=updated_task.status.as_generic_type(),
                )
            )

            await uow.commit()

            return updated_task


class DeleteTaskCommandHandler(TasksCommandHandler[DeleteTaskCommand]):
    async def __call__(self, command: DeleteTaskCommand) -> None:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)
            deleted_task: None = await task_service.delete(command.oid)

            await uow.add_event(
                TaskDeletedEvent(task_id=command.oid)
            )

            await uow.commit()

            return deleted_task


class UpdateTaskStatusCommandHandler(TasksCommandHandler[UpdateTaskStatusCommand]):
    async def __call__(self, command: UpdateTaskStatusCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)

            existing_task: TaskEntity = await task_service.get_by_task_id(command.task_id)
            existing_task.status = TaskStatus(command.status)

            updated_task: TaskEntity = await task_service.update(oid=command.task_id, model=existing_task)

            await uow.add_event(
                TaskUpdatedEvent(
                    task_id=updated_task.oid,
                    email_assigned_to=updated_task.assigned_to.email.as_generic_type(),
                    start_datetime=updated_task.start_datetime,
                    end_datetime=updated_task.due_datetime,
                    status=updated_task.status.as_generic_type(),
                )
            )

            await uow.commit()

            return updated_task


class CreateNewCommentForTaskCommandHandler(TasksCommandHandler[CreateNewCommentForTaskCommand]):
    async def __call__(self, command: CreateNewCommentForTaskCommand) -> TaskEntity:
        async with self._uow as uow:
            task_service: TasksService = TasksService(uow=self._uow)
            existing_task: TaskEntity = await task_service.get_by_task_id(command.task_id)
            existing_task.comments.append(Comment(command.comment))

            updated_task: TaskEntity = await task_service.update(oid=command.task_id, model=existing_task)
            await uow.commit()

            return updated_task
