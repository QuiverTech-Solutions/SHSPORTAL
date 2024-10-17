"""Routes to manage roles."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.role import RoleRepository
from src.models.role import RoleCreate, RolePublic, RoleUpdate

role_router = APIRouter()


@role_router.post(
    "/",
    response_model=RolePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    new_role: RoleCreate,
    role_repo: RoleRepository = Depends(get_repository(RoleRepository)),
) -> RolePublic:
    """Create a new role."""
    return await role_repo.create_role(new_role=new_role)


@role_router.get(
    "/{id}",
    response_model=RolePublic,
    status_code=status.HTTP_200_OK,
)
async def get_role(
    id: UUID,
    role_repo: RoleRepository = Depends(get_repository(RoleRepository)),
) -> RolePublic:
    """Get a role by its ID."""
    return await role_repo.get_role(id=id)


@role_router.get(
    "/",
    response_model=List[RolePublic],
    status_code=status.HTTP_200_OK,
)
async def get_roles(
    role_repo: RoleRepository = Depends(get_repository(RoleRepository)),
) -> List[RolePublic]:
    """Get all roles."""
    return await role_repo.get_roles()


@role_router.put(
    "/{id}",
    response_model=RolePublic,
    status_code=status.HTTP_200_OK,
)
async def update_role(
    id: UUID,
    role_update: RoleUpdate,
    role_repo: RoleRepository = Depends(get_repository(RoleRepository)),
) -> RolePublic:
    """Update a role."""
    return await role_repo.update_role(id=id, role_update=role_update)


@role_router.delete(
    "/{id}",
    response_model=RolePublic,
    status_code=status.HTTP_200_OK,
)
async def delete_role(
    id: UUID,
    role_repo: RoleRepository = Depends(get_repository(RoleRepository)),
) -> RolePublic:
    """Delete a role."""
    return await role_repo.delete_role(id=id)
