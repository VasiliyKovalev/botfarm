import warnings
from typing import Literal

from pydantic import PostgresDsn, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


ENV_FILE_NAME = ".env"


class Settings(BaseSettings):
    """
    Конфигурация настроек приложения.

    Загружает настройки из переменных окружения с валидацией.
    """
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    SECRET_KEY: str = "changethis"

    PROJECT_NAME: str = "botfarm"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = "changethis"
    POSTGRES_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Строит URI для подключения к PostgreSQL для SQLAlchemy с asyncpg.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def TEST_SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username="botfarm_user_test",
            password="password_test",
            host="localhost",
            port=5433,
            path="botfarm_db_test",
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'Значение {var_name} равно "changethis", '
                "для безопасности измените его по крайней мере для продакшена."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)

        return self


settings = Settings()  # type: ignore
