"""Routes to manage schools."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.school import SchoolRepository
from src.models.schools import SchoolCreate, SchoolPublic, SchoolUpdate

school_router = APIRouter()


@school_router.post(
    "/",
    response_model=SchoolPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_school(
    new_school: SchoolCreate,
    school_repo: SchoolRepository = Depends(get_repository(SchoolRepository)),
) -> SchoolPublic:
    """Create a new school."""
    return await school_repo.create_school(new_school=new_school)


@school_router.get(
    "/{id}",
    response_model=SchoolPublic,
    status_code=status.HTTP_200_OK,
)
async def get_school(
    id: UUID,
    school_repo: SchoolRepository = Depends(get_repository(SchoolRepository)),
) -> SchoolPublic:
    """Get a school by its ID."""
    return await school_repo.get_school_by_id(id=id)


@school_router.put(
    "/{id}",
    response_model=SchoolPublic,
    status_code=status.HTTP_200_OK,
)
async def update_school(
    id: UUID,
    school_update: SchoolUpdate,
    school_repo: SchoolRepository = Depends(get_repository(SchoolRepository)),
) -> SchoolPublic:
    """Update a school."""
    return await school_repo.update_school(id=id, school_update=school_update)


@school_router.delete(
    "/{id}",
    response_model=SchoolPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_school(
    id: UUID,
    school_repo: SchoolRepository = Depends(get_repository(SchoolRepository)),
) -> SchoolPublic:
    """Delete a school."""
    return await school_repo.delete_school(id=id)
