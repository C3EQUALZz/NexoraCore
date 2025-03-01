from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.shared import URL


@dataclass(eq=False)
class SocialNetworkEntity(BaseEntity):
    platform: str
    url: URL
