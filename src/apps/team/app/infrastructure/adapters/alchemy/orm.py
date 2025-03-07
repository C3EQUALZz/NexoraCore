from sqlalchemy import MetaData, UUID, Index, DateTime, func
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import registry, relationship

from app.infrastructure.adapters.alchemy.typed_decorators import TeamNameTypedDecorator, TeamDescriptionTypedDecorator, \
    TeamMemberPositionTypedDecorator

metadata: MetaData = MetaData()
mapper_registry: registry = registry(metadata=metadata)

# Таблица команд
team_table = Table(
    "teams",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("name", TeamNameTypedDecorator(30), unique=True, nullable=False),
    Column("description", TeamDescriptionTypedDecorator, nullable=True),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)

# Таблица членов команды
team_member_table = Table(
    "team_members",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("team_id", UUID(as_uuid=True), ForeignKey("teams.oid"), nullable=False),
    Column("position", TeamMemberPositionTypedDecorator, nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()),
    UniqueConstraint("user_id", "team_id", name="uq_user_team")
)

# Таблица связей начальников и подчинённых
team_hierarchy_table = Table(
    "team_hierarchy",
    metadata,
    Column("superior_id", UUID(as_uuid=True), ForeignKey("team_members.oid", ondelete="SET NULL"), nullable=True),
    Column("subordinate_id", UUID(as_uuid=True), ForeignKey("team_members.oid", ondelete="SET NULL"), nullable=True),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()),
    UniqueConstraint("superior_id", "subordinate_id", name="uq_team_hierarchy"),
    Index("ix_superior_subordinate", "superior_id", "subordinate_id")
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.team_members import TeamMemberEntity
    from app.domain.entities.team import TeamEntity

    mapper_registry.map_imperatively(
        TeamEntity,
        team_table,
        properties={
            "members": relationship(TeamMemberEntity, backref="team", lazy="selectin"),
            "oid": team_table.c.oid
        }
    )

    mapper_registry.map_imperatively(
        TeamMemberEntity,
        team_member_table,
        properties={
            "user": team_member_table.c.user_id,
            "superiors": relationship(
                TeamMemberEntity,
                secondary=team_hierarchy_table,
                primaryjoin=team_member_table.c.oid == team_hierarchy_table.c.subordinate_id,
                secondaryjoin=team_member_table.c.oid == team_hierarchy_table.c.superior_id,
                back_populates="subordinates",  # Вместо backref
                lazy="selectin",
            ),
            "subordinates": relationship(
                TeamMemberEntity,
                secondary=team_hierarchy_table,
                primaryjoin=team_member_table.c.oid == team_hierarchy_table.c.superior_id,
                secondaryjoin=team_member_table.c.oid == team_hierarchy_table.c.subordinate_id,
                back_populates="superiors",
                lazy="selectin",
            ),
            "oid": team_member_table.c.oid
        },
    )
