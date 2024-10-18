"""User role repository."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies.database import get_repository
from src.db.repositories.user_role import UserRoleRepository
from src.models.user_role import UserRolesCreate, UserRolesPublic

user_roles_router = APIRouter()
audit_logger = logging.getLogger("audit")


@user_roles_router.post(
    "/user-roles",
    response_model=UserRolesPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_role(
    user_role_create: UserRolesCreate,
    user_roles_repo: UserRoleRepository = Depends(get_repository(UserRoleRepository)),
) -> UserRolesPublic:
    """Create a new user role."""
    return await user_roles_repo.assign_role_to_user(new_user_role=user_role_create)


@user_roles_router.get(
    "/user-roles/{role_id}",
    response_model=UserRolesPublic,
    status_code=status.HTTP_200_OK,
)
async def get_user_role(
    role_id: UUID,
    user_roles_repo: UserRoleRepository = Depends(get_repository(UserRoleRepository)),
) -> UserRolesPublic:
    """Get a user role by ID."""
    return await user_roles_repo.get_user_roles(role_id=role_id)


@user_roles_router.delete(
    "/user-roles/{role_id}",
    response_model=UserRolesPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_user_role(
    role_id: UUID,
    user_roles_repo: UserRoleRepository = Depends(get_repository(UserRoleRepository)),
) -> UserRolesPublic:
    """Delete a user role."""
    return await user_roles_repo.delete_user_role(role_id=role_id)
