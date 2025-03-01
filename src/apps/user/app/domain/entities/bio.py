from dataclasses import dataclass, field

from app.domain.entities.address import Address
from app.domain.entities.base import BaseEntity
from app.domain.entities.social_network import SocialNetwork
from app.domain.entities.user import UserEntity
from app.domain.values.bio import Gender, PhoneNumber
from app.domain.values.shared import URL


@dataclass(eq=False)
class BioEntity(BaseEntity):
    user: UserEntity
    phone_number: PhoneNumber
    photo: URL
    gender: Gender
    address: Address
    social_networks: list[SocialNetwork] = field(default_factory=list)
