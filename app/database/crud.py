import uuid
from datetime import datetime
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.database.models.user import User
from app.schemas.user import UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    result = await session.execute(
        select(User).where(User.login == user_create.login)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким login уже существует."
        )

    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        login=user_create.login,
        password=hashed_password,
        project_id=user_create.project_id,
        env=user_create.env,
        domain=user_create.domain
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_id(
    session: AsyncSession,
    user_id: uuid.UUID
) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_or_404(session: AsyncSession, user_id: uuid.UUID) -> User:
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )
    return user


async def get_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def acquire_lock(session: AsyncSession, user_id: uuid.UUID) -> None:
    user = await get_user_or_404(session, user_id)

    if user.locktime is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже заблокирован."
        )

    user.locktime = datetime.now()
    await session.commit()


async def release_lock(session: AsyncSession, user_id: uuid.UUID) -> None:
    user = await get_user_or_404(session, user_id)

    user.locktime = None
    await session.commit()
