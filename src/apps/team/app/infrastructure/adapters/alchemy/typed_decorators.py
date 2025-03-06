from sqlalchemy.types import TypeDecorator
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy import String

from app.domain.values.team import TeamName, TeamDescription
from app.domain.values.team_members import TeamMemberPosition
from app.exceptions.infrastructure import ConvertingException


class TeamNameTypedDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: TeamName, dialect: Dialect) -> str:
        if value is not None and isinstance(value, TeamName):
            return value.as_generic_type()
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> TeamName:
        if column is not None:
            return TeamName(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class TeamDescriptionTypedDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: TeamDescription, dialect: Dialect) -> str:
        if value is not None and isinstance(value, TeamDescription):
            return value.as_generic_type()
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> TeamDescription:
        if column is not None:
            return TeamDescription(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class TeamMemberPositionTypedDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: TeamMemberPosition, dialect: Dialect) -> str:
        if value is not None and isinstance(value, TeamMemberPosition):
            return value.as_generic_type()
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> TeamMemberPosition:
        if column is not None:
            return TeamMemberPosition(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")
