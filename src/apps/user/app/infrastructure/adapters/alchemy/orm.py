from sqlalchemy import Table, Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.adapters.alchemy.metadata import metadata, mapper_registry

roles_table = Table(
    "roles",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(50), nullable=False, unique=True)
)

statuses_table = Table(
    "statuses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(50), nullable=False, unique=True)
)

users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("surname", String(100)),
    Column("name", String(100), nullable=False),
    Column("patronymic", String(100)),
    Column("email", String(100), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", onupdate='CASCADE', ondelete='CASCADE'),
           nullable=False),
    Column("status_id", UUID(as_uuid=True), ForeignKey("statuses.id", onupdate='CASCADE', ondelete='CASCADE'),
           nullable=False),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)

bios_table = Table(
    "bios",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", onupdate='CASCADE', ondelete='CASCADE'), unique=True),
    Column("phone_number", String(20)),
    Column("photo_url", String(255)),
    Column("gender", String(10)),
    Column("social_networks", JSON),  # Хранение списка социальных сетей
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)

addresses_table = Table(
    "addresses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("bio_id", UUID(as_uuid=True), ForeignKey("bios.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column("country", String(100)),
    Column("city", String(100)),
    Column("street", String(100)),
    Column("postal_code", String(20)),
)

social_networks_table = Table(
    "social_networks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("bio_id", UUID(as_uuid=True), ForeignKey("bios.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column("platform", String(50), nullable=False),
    Column("url", String(255), nullable=False),
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.user import UserEntity
    from app.domain.entities.bio import BioEntity
    from app.domain.entities.address import AddressEntity
    from app.domain.entities.social_network import SocialNetworkEntity
    from app.domain.values.user import Role
    from app.domain.values.user import Status

    mapper_registry.map_imperatively(Role, roles_table)
    mapper_registry.map_imperatively(Status, statuses_table)
    mapper_registry.map_imperatively(AddressEntity, addresses_table)
    mapper_registry.map_imperatively(SocialNetworkEntity, social_networks_table)
    mapper_registry.map_imperatively(UserEntity, users_table)
    mapper_registry.map_imperatively(BioEntity, bios_table)
