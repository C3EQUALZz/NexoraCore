from dataclasses import dataclass
from app.domain.entities.base import BaseEntity
from app.domain.values.score import ScoreValue, Criteria
from app.domain.values.shared import Comment


@dataclass(eq=False)
class Score(BaseEntity):
    value: ScoreValue
    criteria: Criteria
    comment: Comment
