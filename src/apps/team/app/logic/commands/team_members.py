from dataclasses import dataclass, field

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateTeamMemberCommand(AbstractCommand):
    user_id: str
    position: str
    superiors: list[str] = field(default_factory=list)
    subordinates: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class UpdateTeamMemberCommand(AbstractCommand):
    oid: str
    user_id: str
    position: str
    superiors: list[str] = field(default_factory=list)
    subordinates: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DeleteTeamMemberCommand(AbstractCommand):
    oid: str
