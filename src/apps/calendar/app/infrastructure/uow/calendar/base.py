from abc import ABC

from app.infrastructure.repositories.calendar.base import CalendarsRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class CalendarUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with calendar, that is used by service layer of calendars module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """
    calendar: CalendarsRepository