from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateTeamMemberCommand(AbstractCommand):
    user_id: str
    team_id: str
    position: str
    superiors: list[str]
    subordinates: list[str]


@dataclass(frozen=True)
class UpdateTeamMemberCommand(AbstractCommand):
    oid: str
    user_id: str
    position: str
    superiors: list[str]
    subordinates: list[str]


@dataclass(frozen=True)
class DeleteTeamMemberCommand(AbstractCommand):
    user_id: str
    team_id: str
