from app.infrastructure.uow.events.base import EventsUnitOfWork


class EventsViews:
    """
    Views related to users, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.
    """

    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow: EventsUnitOfWork = uow
