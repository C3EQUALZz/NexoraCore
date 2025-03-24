from dataclasses import dataclass
from datetime import datetime

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateTaskCommand(AbstractCommand):
    title: str
    description: str
    assigned_to: str
    created_by: str
    due_datetime: datetime


@dataclass(frozen=True)
class UpdateTaskCommand(AbstractCommand):
    oid: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    due_datetime: datetime
    status: str


@dataclass(frozen=True)
class DeleteTaskCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class CreateCommentForTaskCommand(AbstractCommand):
    task_id: str
    comment: str


@dataclass(frozen=True)
class UpdateTaskStatusCommand(AbstractCommand):
    task_id: str
    status: str
