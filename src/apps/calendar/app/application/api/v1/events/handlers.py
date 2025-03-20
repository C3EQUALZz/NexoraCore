from fastapi import APIRouter
from uuid import UUID

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get(
    "/{event_id}/",
    description="Get event in calendar by ID"
)
async def get_event_in_calendar(event_id: UUID):
    ...


@router.get(
    "/",
    description="Get all events in calendar"
)
async def get_all_events_in_calendar():
    ...


@router.post(
    "/",
    description="Create new event in calendar"
)
async def create_event_in_calendar():
    ...


@router.put(
    "/{event_id}/",
    description="Update event in calendar"
)
async def update_event_in_calendar(event_id: UUID):
    ...




