from app.logic.commands.base import AbstractCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class GreateEventInCalendar(AbstractCommand):
    ...
