import enum
import re
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database.models.base import Base


LOGIN_MAX_LENGTH = 255
PASSWORD_MAX_LENGTH = 255


class EnvUser(str, enum.Enum):
    """Допустимые окружения для пользователя."""
    PROD = "prod"
    PREPROD = "preprod"
    STAGE = "stage"


class DomainUser(str, enum.Enum):
    """Типы пользователей."""
    REGULAR = "regular"
    CANARY = "canary"


class User(Base):
    """Модель пользователя ботофермы."""
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(
        String(LOGIN_MAX_LENGTH),
        unique=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(PASSWORD_MAX_LENGTH),
        nullable=False
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    env: Mapped[EnvUser] = mapped_column(
        Enum(EnvUser),
        nullable=False,
    )

    domain: Mapped[DomainUser] = mapped_column(
        Enum(DomainUser),
        nullable=False,
        default=DomainUser.REGULAR
    )

    locktime: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    @validates('login')
    def validate_login(self, key: str, value: str) -> str:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError(f"Некорректный формат email: {value}")

        return value
