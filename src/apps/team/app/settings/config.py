from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field, RedisDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class CommonSettings(BaseSettings, ABC):
    """
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DatabaseSettings(CommonSettings):
    """
    Настройки для подключения к базе данных.
    Здесь есть параметры Optional с той целью, потому что может использоваться sqlite.
    """

    host: str | None = Field(alias="DATABASE_HOST", default=None)
    port: int | None = Field(alias="DATABASE_PORT_NETWORK", default=None)
    user: str | None = Field(alias="DATABASE_USER", default=None)
    password: str | None = Field(alias="DATABASE_PASSWORD", default=None)
    name: str = Field(alias="DATABASE_NAME")

    @property
    def url(self) -> str:
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/"


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class AdminSettings(CommonSettings):
    email: str = Field(alias="ADMIN_EMAIL")
    surname: str = Field(alias="ADMIN_SURNAME")
    name: str = Field(alias="ADMIN_NAME")
    patronymic: str = Field(alias="ADMIN_PATRONYMIC")
    password: str = Field(alias="ADMIN_PASSWORD")
    telegram_uri: str = Field(alias="ADMIN_TELEGRAM_URI")


class AuthSettings(CommonSettings):
    public_key: str = Field(alias="PUBLIC_KEY")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")


class HttpxSettings(CommonSettings):
    max_connections: int = Field(default=500, alias="MAX_CONNECTIONS")
    max_keepalive_connections: int = Field(default=50, alias="MAX_KEEPALIVE_CONNECTIONS")
    keepalive_expiry: float = Field(default=30.0, alias="KEEPALIVE_EXPIRY")
    timeout: float = Field(default=20.0, alias="TIMEOUT")

    user_endpoint_url: str = Field(
        default="http://user-service-app-backend:8000/api/v1/users",
        alias="MICROSERVICE_USER"
    )


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    database: DatabaseSettings = DatabaseSettings()
    cache: RedisSettings = RedisSettings()
    admin: AdminSettings = AdminSettings()
    client: HttpxSettings = HttpxSettings()
    auth: AuthSettings = AuthSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
