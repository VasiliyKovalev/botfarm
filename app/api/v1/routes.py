import uuid

from fastapi import APIRouter, status

from app.core.dependencies import UserServiceDep
from app.schemas.user import UserCreate, UserResponse


router = APIRouter()


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_create: UserCreate,
    user_service: UserServiceDep
):
    return await user_service.create_user(user_create)


@router.get("/users", response_model=list[UserResponse])
async def get_users(user_service: UserServiceDep):
    return await user_service.get_users()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    user_service: UserServiceDep
):
    return await user_service.get_user(user_id)


@router.post("/users/{user_id}/acquire_lock")
async def acquire_lock(
    user_id: uuid.UUID,
    user_service: UserServiceDep
):
    await user_service.acquire_lock(user_id)
    return {"message": "Пользователь заблокирован."}


@router.post("/users/{user_id}/release_lock")
async def release_lock(
    user_id: uuid.UUID,
    user_service: UserServiceDep
):
    await user_service.release_lock(user_id)
    return {"message": "Пользователь разблокирован."}
