from typing import Literal

from sqlalchemy import TypeDecorator, String, Dialect, LargeBinary

from app.domain.values.bio import PhoneNumber, Gender
from app.domain.values.shared import URL
from app.domain.values.user import Email, Password
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


class EmailTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, fields: dict[Literal["value"], str], dialect: Dialect) -> str:
        if fields is not None and fields.get("value") is not None:
            return fields["value"]
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, fields: {fields}")

    def process_result_value(self, column: str, dialect: Dialect) -> Email:
        if column is not None:
            return Email(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class PasswordTypeDecorator(TypeDecorator):
    impl = LargeBinary
    cache_ok = True

    def process_bind_param(self, fields: dict[Literal["value"], bytes], dialect: Dialect) -> bytes:
        if fields is not None and fields.get("value") is not None:
            return fields["value"]
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, fields: {fields}")

    def process_result_value(self, column: bytes, dialect: Dialect) -> Password:
        if column is not None:
            return Password(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class GenderTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, fields: dict[Literal["value"], str], dialect: Dialect) -> str:
        if fields is not None and fields.get("value") is not None:
            return fields["value"]
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, fields: {fields}")

    def process_result_value(self, column: str, dialect: Dialect) -> Gender:
        if column is not None:
            return Gender(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class URLTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, fields: dict[Literal["value"], str], dialect: Dialect) -> str:
        if fields is not None and fields.get("value") is not None:
            return fields["value"]
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, fields: {fields}")

    def process_result_value(self, column: str, dialect: Dialect) -> URL:
        if column is not None:
            return URL(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")