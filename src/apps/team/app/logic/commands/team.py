from app.logic.commands.base import AbstractCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTeamCommand(AbstractCommand):
    name: str
    description: str


@dataclass(frozen=True)
class UpdateTeamCommand(AbstractCommand):
    oid: str
    name: str
    description: str


@dataclass(frozen=True)
class DeleteTeamCommand(AbstractCommand):
    oid: str
