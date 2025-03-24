from dataclasses import dataclass
from datetime import datetime

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateMeetingCommand(AbstractCommand):
    organizer_id: str
    participant_ids: list[str]
    start_time: datetime
    end_time: datetime
    title: str
    description: str


@dataclass(frozen=True)
class DeleteMeetingCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class UpdateMeetingCommand(CreateMeetingCommand):
    oid: str
