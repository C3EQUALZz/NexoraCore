from uuid import UUID

from fastapi import APIRouter
from datetime import date

router = APIRouter(
    prefix="/employees",
)


@router.get("/{employee_id}/events/monthly/{month}")
async def get_all_events_for_user_by_month(employee_id: UUID, month: int):
    ...


@router.get("/{employee_id}/events/daily/")
async def get_all_events_for_user_by_day(employee_id: UUID, day: date):
    ...
