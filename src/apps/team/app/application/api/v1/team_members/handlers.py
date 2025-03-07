from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

router = APIRouter(prefix="/{team_id}/members", tags=["team_members"], route_class=DishkaRoute)


@router.post(
    "/",
    status_code=201,
    description="Add user to the team",
)
async def create_team_member():
    ...


@router.get(
    "/",
    status_code=200,
    description="Get all team members",
)
async def get_all_team_members():
    ...


@router.delete(
    "/{user_id}/",
    status_code=204,
    description="Delete a team member"
)
async def delete_team_member(user_id: str):
    ...


@router.put(
    "/{user_id}/",
    status_code=200,
)
async def update_team_member_role(user_id: str):
    ...
