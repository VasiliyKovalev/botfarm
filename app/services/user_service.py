import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.schemas.user import UserCreate, UserResponse


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        db_user = await crud.create_user(self.session, user_create)
        return UserResponse.model_validate(db_user)

    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        db_user = await crud.get_user_or_404(self.session, user_id)
        return UserResponse.model_validate(db_user)

    async def get_users(self) -> Sequence[UserResponse]:
        db_users = await crud.get_users(self.session)
        return [UserResponse.model_validate(user) for user in db_users]

    async def acquire_lock(self, user_id: uuid.UUID) -> None:
        await crud.acquire_lock(self.session, user_id)

    async def release_lock(self, user_id: uuid.UUID) -> None:
        await crud.release_lock(self.session, user_id)
