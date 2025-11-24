import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.database.models.user import EnvUser, DomainUser


class UserCreate(BaseModel):
    """Схема для создания пользователя."""
    login: EmailStr
    password: str = Field(..., min_length=6)
    project_id: uuid.UUID
    env: EnvUser
    domain: DomainUser = DomainUser.REGULAR


class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя."""
    id: uuid.UUID
    login: EmailStr
    project_id: uuid.UUID
    env: EnvUser
    domain: DomainUser
    created_at: datetime
    locktime: datetime | None

    model_config = {'from_attributes': True}
