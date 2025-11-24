from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.user_service import UserService


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserService:
    """
    Dependency Injection для получения сервиса пользователей.
    """
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
