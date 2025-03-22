import uuid

from sqlalchemy import (
    Column, String, DateTime, Text, ForeignKey, Table,
    UUID, CheckConstraint, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Ассоциационная таблица для участников встреч
meeting_participants = Table(
    'meeting_participants',
    Base.metadata,
    Column(
        'meeting_id',
        UUID(as_uuid=True),
        ForeignKey('meetings.oid'), primary_key=True),
    Column(
        'user_id',
        UUID(as_uuid=True),
        ForeignKey('users.oid'), primary_key=True)
)


class UserModel(Base):
    __tablename__ = 'users'
    oid = Column(UUID(as_uuid=True), primary_key=True,
                 default=uuid.uuid4, unique=True)
    created_at = Column(DateTime(timezone=True),
                        default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class CalendarModel(Base):
    __tablename__ = 'calendars'
    oid = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.oid'), unique=True)

    meetings = relationship("MeetingModel", back_populates="calendar", cascade="all, delete-orphan")
    tasks = relationship(
        "TaskModel",
        back_populates="calendar",
        cascade="all, delete-orphan",
        foreign_keys="TaskModel.calendar_id"  # Явно указываем foreign key
    )


class BaseEventModel(Base):
    __abstract__ = True
    oid = Column(UUID(as_uuid=True), primary_key=True,
                 default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('end_time > start_time',
                        name='check_end_after_start'),
    )


class MeetingModel(BaseEventModel):
    __tablename__ = 'meetings'

    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.oid'))
    calendar_id = Column(UUID(as_uuid=True), ForeignKey('calendars.oid'))

    # Relationships
    calendar = relationship("CalendarModel", back_populates="meetings")
    participants = relationship("UserModel", secondary=meeting_participants, backref="participating_meetings")


class TaskModel(BaseEventModel):
    __tablename__ = 'tasks'

    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.oid'))
    assignee_id = Column(UUID(as_uuid=True), ForeignKey('users.oid'))
    calendar_id = Column(UUID(as_uuid=True), ForeignKey('calendars.oid'))  # Добавляем явный ForeignKey
    status = Column(String(20), default='pending')

    # Relationships
    calendar = relationship(
        "CalendarModel",
        back_populates="tasks",
        foreign_keys=[calendar_id]  # Явно указываем foreign key
    )

    created_by = relationship("UserModel", foreign_keys=[created_by_id])
    assignee = relationship("UserModel", foreign_keys=[assignee_id])