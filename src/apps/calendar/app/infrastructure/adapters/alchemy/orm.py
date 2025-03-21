from sqlalchemy import MetaData
from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

metadata: MetaData = MetaData()
mapper_registry: registry = registry(metadata=metadata)

users_table = Table(
    'users',
    metadata,
    Column('id', String, primary_key=True)
)

# calendars
calendars_table = Table(
    'calendars',
    metadata,
    Column('id', String, primary_key=True),
    Column('owner_id', String, ForeignKey('users.id')),
)

# base events table (joined table inheritance)
events_table = Table(
    'events',
    metadata,
    Column('id', String, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', Text),
    Column('start_time', DateTime, nullable=False),
    Column('end_time', DateTime, nullable=False),
    Column('created_by', String, ForeignKey('users.id')),
    Column('owner_id', String, ForeignKey('users.id')),
    Column('type', String(50)),  # для полиморфизма
)

# meetings
meetings_table = Table(
    'meetings',
    metadata,
    Column('id', String, ForeignKey('events.id'), primary_key=True),
    Column('organizer_id', String, ForeignKey('users.id'), nullable=False),
)

# participants in meetings
meeting_participants_table = Table(
    'meeting_participants',
    metadata,
    Column('meeting_id', String, ForeignKey('meetings.id'), primary_key=True),
    Column('participant_id', String, ForeignKey('users.id'), primary_key=True),
)

tasks_table = Table(
    'tasks',
    metadata,
    Column('id', String, ForeignKey('events.id'), primary_key=True),
    Column('assignee_id', String, ForeignKey('users.id')),
    Column('status', String(50), nullable=False),
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.user import UserEntity
    from app.domain.entities.calendar import CalendarEntity
    from app.domain.entities.events.base import BaseEventCalendarEntity
    from app.domain.entities.events.meeting import MeetingEntity
    from app.domain.entities.events.task import TaskEntity

    mapper_registry.map_imperatively(
        UserEntity,
        users_table
    )

    # CalendarEntity ➜ владелец календаря
    mapper_registry.map_imperatively(
        CalendarEntity,
        calendars_table,
        properties={
            'owner': relationship(UserEntity, backref='calendars')
        }
    )

    mapper_registry.map_imperatively(
        BaseEventCalendarEntity,
        events_table,
        polymorphic_on=events_table.c.type,
        polymorphic_identity='base_event',
        properties={
            'created_by_user': relationship(UserEntity, foreign_keys=[events_table.c.created_by]),
            'owner': relationship(UserEntity, foreign_keys=[events_table.c.owner_id]),
        }
    )

    mapper_registry.map_imperatively(
        MeetingEntity,
        meetings_table,
        inherits=BaseEventCalendarEntity,
        polymorphic_identity='meeting',
        properties={
            'organizer': relationship(UserEntity, foreign_keys=[meetings_table.c.organizer_id]),
            'participants': relationship(
                UserEntity,
                secondary=meeting_participants_table,
                backref='meetings_participated'
            )
        }
    )

    mapper_registry.map_imperatively(
        TaskEntity,
        tasks_table,
        inherits=BaseEventCalendarEntity,
        polymorphic_identity='task',
        properties={
            'assignee': relationship(UserEntity, foreign_keys=[tasks_table.c.assignee_id])
        }
    )

    mapper_registry.map_imperatively(
        CalendarEntity,
        calendars_table,
        properties={
            'events': relationship(
                BaseEventCalendarEntity,
                primaryjoin=calendars_table.c.owner_id == events_table.c.owner_id,
                foreign_keys=[events_table.c.owner_id]
            )
        }
    )
