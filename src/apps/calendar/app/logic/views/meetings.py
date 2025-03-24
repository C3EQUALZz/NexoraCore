from app.domain.entities.events.meeting import MeetingEntity
from app.infrastructure.services.meetings import MeetingsService
from app.infrastructure.uow.events.base import EventsUnitOfWork


class MeetingsView:
    """
    Views related to meetings, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.
    """

    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow: EventsUnitOfWork = uow

    async def get_meeting_by_id(self, meeting_id: str) -> MeetingEntity:
        meetings_service: MeetingsService = MeetingsService(self._uow)
        return await meetings_service.get_by_oid(meeting_id)

    async def get_all_meetings(
            self,
            page_number: int | None = None,
            page_size: int | None = None
    ) -> list[MeetingEntity]:
        meetings_service: MeetingsService = MeetingsService(self._uow)
        start: int | None = None
        limit: int | None = None

        if page_number is not None and page_size is not None:
            start = (page_number - 1) * page_size
            limit = start + page_size

        return await meetings_service.get_all(start, limit)