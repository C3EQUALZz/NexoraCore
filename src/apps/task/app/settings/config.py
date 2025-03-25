from abc import ABC
from pathlib import Path

from pydantic import Field
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

    calendar_endpoint_url: str = Field(
        default="http://calendar-service-app-backend:8004/api/v1/calendar",
        alias="MICROSERVICE_CALENDAR"
    )


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    database: DatabaseSettings = DatabaseSettings()
    broker: BrokerSettings = BrokerSettings()
    client: HttpxSettings = HttpxSettings()
    auth: AuthSettings = AuthSettings()
