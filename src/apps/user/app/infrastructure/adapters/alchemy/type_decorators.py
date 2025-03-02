from typing import Literal

from sqlalchemy import TypeDecorator, String, Dialect

from app.domain.values.bio import PhoneNumber
from app.exceptions.infrastructure import ConvertingException


class PhoneNumberTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, fields: dict[Literal["value"], str], dialect: Dialect) -> str:
        if fields is not None and fields.get("value") is not None:
            return fields["value"]
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, fields: {fields}")

    def process_result_value(self, column: str, dialect: Dialect) -> PhoneNumber:
        if column is not None:
            return PhoneNumber(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")
