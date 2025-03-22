from dataclasses import dataclass
from datetime import datetime

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateTaskCommand(AbstractCommand):
    title: str
    description: str
    assignee_id: str
    start_time: datetime
    end_time: datetime
    created_by_id: str


@dataclass(frozen=True)
class DeleteTaskCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class UpdateTaskCommand(AbstractCommand):
    oid: str
    title: str
    description: str | None
    assignee_id: str
    start_time: datetime
    end_time: datetime
    status: str
