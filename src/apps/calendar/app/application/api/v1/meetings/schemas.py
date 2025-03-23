from datetime import datetime, UTC
from typing import Self

from pydantic import BaseModel, model_validator

from app.application.api.v1.utils.schemas import StringUUID, UserSchemaResponse
from app.domain.entities.events.meeting import MeetingEntity


class CreateMeetingSchemaRequest(BaseModel):
    organizer_id: StringUUID
    participant_ids: list[StringUUID]
    start_time: datetime
    end_time: datetime
    title: str
    description: str

    @model_validator(mode="after")
    def check_time_fields(self) -> Self:
        now: datetime = datetime.now(self.start_time.tzinfo) if self.start_time.tzinfo else datetime.now(UTC)

        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")

        if self.start_time < now or self.end_time < now:
            raise ValueError("You can set meeting in the past")

        return self


class UpdateMeetingSchemaRequest(CreateMeetingSchemaRequest):
    oid: StringUUID


class MeetingSchemaResponse(BaseModel):
    oid: StringUUID
    organizer: UserSchemaResponse
    participants: list[UserSchemaResponse]
    start_time: datetime
    end_time: datetime
    title: str
    description: str

    @model_validator(mode="after")
    def check_time_fields(self) -> Self:
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")

        return self

    @classmethod
    def from_entity(cls, entity: MeetingEntity) -> Self:
        return cls(
            oid=entity.oid,
            organizer=UserSchemaResponse.from_entity(entity.organizer),
            participants=[UserSchemaResponse.from_entity(x) for x in entity.participants],
            start_time=entity.start_time,
            end_time=entity.end_time,
            title=entity.title,
            description=entity.description,
        )
