"""Users related routes."""
# import logging
# from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

# from src.api.dependencies.database import get_repository
# from src.db.repositories.users import UsersRepository  # Assuming you have a UsersRepository
# from src.models.users import UserCreate, UserPublic, UserUpdate

users_router = APIRouter()
# audit_logger = logging.getLogger("audit")


# @users_router.post(
#     "/users",
#     response_model=UserPublic,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_user(
#     user_create: UserCreate,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Create a new user."""
#     return await users_repo.create_user(new_user=user_create)


# @users_router.get(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def get_user(
#     user_id: UUID,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Get a user by ID."""
#     return await users_repo.get_user_by_id(user_id=user_id)


# @users_router.put(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def update_user(
#     user_id: UUID,
#     user_update: UserUpdate,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Update a user."""
#     return await users_repo.update_user(user_id=user_id, user_update=user_update)


# @users_router.delete(
#     "/users/{user_id}",
#     response_model=UserPublic,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_user(
#     user_id: UUID,
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     """Delete a user."""
#     return await users_repo.delete_user(user_id=user_id)
