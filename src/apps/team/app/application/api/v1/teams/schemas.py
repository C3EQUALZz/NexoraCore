from pydantic import BaseModel, Field


class CreateTeamSchemaRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)


class CreateTeamResponse(BaseModel):
    ...
