"""Routes to manage students."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.students import StudentRepository
from src.models.students import StudentCreate, StudentPublic, StudentUpdate

student_router = APIRouter()


@student_router.post(
    "/",
    response_model=StudentPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    new_student: StudentCreate,
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentPublic:
    """Create a new student."""
    return await student_repo.create_student(new_student=new_student)


@student_router.get(
    "/{id}",
    response_model=StudentPublic,
    status_code=status.HTTP_200_OK,
)
async def get_student(
    id: UUID,
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentPublic:
    """Get a student by their ID."""
    return await student_repo.get_student_by_id(id=id)


@student_router.put(
    "/{id}",
    response_model=StudentPublic,
    status_code=status.HTTP_200_OK,
)
async def update_student(
    id: UUID,
    student_update: StudentUpdate,
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentPublic:
    """Update a student."""
    return await student_repo.update_student(id=id, student_update=student_update)


@student_router.delete(
    "/{id}",
    response_model=StudentPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_student(
    id: UUID,
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentPublic:
    """Delete a student."""
    return await student_repo.delete_student(id=id)
