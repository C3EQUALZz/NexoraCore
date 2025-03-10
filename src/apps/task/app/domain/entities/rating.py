from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.score import Score


@dataclass(eq=False)
class Rating(BaseEntity):
    task_id: str
    user_id: str
    score: list[Score]
