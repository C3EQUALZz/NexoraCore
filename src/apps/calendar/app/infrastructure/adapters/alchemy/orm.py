import uuid
from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, String, DateTime, Text, MetaData, CheckConstraint
from sqlalchemy.orm import registry, relationship

from app.infrastructure.adapters.alchemy.type_decorators import StringUUID

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

# Определение таблиц
users_table = Table(
    'users',
    mapper_registry.metadata,
    Column('oid', StringUUID(), primary_key=True, default=uuid.uuid4),
    Column('created_at', DateTime(timezone=True), default=datetime.now),
    Column('updated_at', DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
)

calendars_table = Table(
    'calendars',
    mapper_registry.metadata,
    Column('oid', StringUUID(), primary_key=True, default=uuid.uuid4),
    Column('owner_id', StringUUID(), ForeignKey('users.oid'), unique=True)
)

tasks_table = Table(
    'tasks',
    mapper_registry.metadata,
    Column('oid', StringUUID(), primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', Text),
    Column('start_time', DateTime(timezone=True), nullable=False),
    Column('end_time', DateTime(timezone=True), nullable=False),
    Column('created_at', DateTime(timezone=True), default=datetime.now),
    Column('updated_at', DateTime(timezone=True), default=datetime.now, onupdate=datetime.now),
    Column('created_by_id', StringUUID(), ForeignKey('users.oid')),
    Column('assignee_id', StringUUID(), ForeignKey('users.oid')),
    Column('calendar_id', StringUUID(), ForeignKey('calendars.oid')),
    Column('status', String(20), default='pending'),
    CheckConstraint('end_time > start_time', name='check_end_after_start')
)

meetings_table = Table(
    'meetings',
    mapper_registry.metadata,
    Column('oid', StringUUID(), primary_key=True, default=uuid.uuid4),
    Column('organizer_id', StringUUID(), ForeignKey('users.oid')),
    Column('calendar_id', StringUUID(), ForeignKey('calendars.oid')),
    Column('title', String(255), nullable=False),
    Column('description', Text),
    Column('start_time', DateTime(timezone=True), nullable=False),
    Column('end_time', DateTime(timezone=True), nullable=False),
    Column('created_at', DateTime(timezone=True), default=datetime.now),
    Column('updated_at', DateTime(timezone=True), default=datetime.now, onupdate=datetime.now),
)

meeting_participants = Table(
    'meeting_participants',
    mapper_registry.metadata,
    Column('meeting_id', StringUUID(), ForeignKey('meetings.oid'), primary_key=True),
    Column('user_id', StringUUID(), ForeignKey('users.oid'), primary_key=True)
)

def start_mappers() -> None:
    from app.domain.entities.user import UserEntity
    from app.domain.entities.calendar import CalendarEntity
    from app.domain.entities.events.task import TaskEntity
    from app.domain.entities.events.meeting import MeetingEntity

    # Маппинг пользователя
    mapper_registry.map_imperatively(
        UserEntity,
        users_table,
        properties={
            'tasks_created': relationship(
                TaskEntity,
                foreign_keys=[tasks_table.c.created_by_id],
                back_populates='created_by'
            ),
            'tasks_assigned': relationship(
                TaskEntity,
                foreign_keys=[tasks_table.c.assignee_id],
                back_populates='assignee'
            )
        }
    )

    # Маппинг календаря
    mapper_registry.map_imperatively(
        CalendarEntity,
        calendars_table,
        properties={
            'tasks': relationship(
                TaskEntity,
                back_populates='calendar',
                foreign_keys=[tasks_table.c.calendar_id]
            ),
            'meetings': relationship(
                MeetingEntity,
                back_populates='calendar'
            )
        }
    )

    # Маппинг задачи
    mapper_registry.map_imperatively(
        TaskEntity,
        tasks_table,
        properties={
            'created_by': relationship(
                UserEntity,
                foreign_keys=[tasks_table.c.created_by_id],
                back_populates='tasks_created',
            ),
            'assignee': relationship(
                UserEntity,
                foreign_keys=[tasks_table.c.assignee_id],
                back_populates='tasks_assigned',
            ),
            'calendar': relationship(
                CalendarEntity,
                back_populates='tasks',
                foreign_keys=[tasks_table.c.calendar_id]
            )
        }
    )

    # Маппинг встречи
    mapper_registry.map_imperatively(
        MeetingEntity,
        meetings_table,
        properties={
            'organizer': relationship(UserEntity),
            'participants': relationship(
                UserEntity,
                secondary=meeting_participants,
                backref='participating_meetings'
            ),
            'calendar': relationship(
                CalendarEntity,
                back_populates='meetings'
            )
        }
    )