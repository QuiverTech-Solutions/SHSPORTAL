"""Student repository."""

import logging
from typing import Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.students import StudentCreate, StudentInDb, StudentUpdate

CREATE_STUDENT_QUERY = """
INSERT INTO students (index_number, name, dob, school_id, location, registration_paid)
VALUES (:index_number, :name, :dob, :school_id, :location, :registration_paid)
RETURNING id, index_number, name, dob, school_id, location, registration_paid, created_at, updated_at, is_deleted
"""

GET_STUDENT_BY_ID_QUERY = """
SELECT id, index_number, name, dob, school_id, location, registration_paid, created_at, updated_at, is_deleted
FROM students
WHERE id = :id AND is_deleted = FALSE
"""

UPDATE_STUDENT_QUERY = """
UPDATE students
SET index_number = :index_number, name = :name, dob = :dob, school_id = :school_id, location = :location, 
    registration_paid = :registration_paid, updated_at = NOW()
WHERE id = :id AND is_deleted = FALSE
RETURNING id, index_number, name, dob, school_id, location, registration_paid, created_at, updated_at, is_deleted
"""

DELETE_STUDENT_BY_ID_QUERY = """
UPDATE students
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, index_number, name, dob, school_id, location, registration_paid, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class StudentRepository(BaseRepository):
    """Student repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for Student repository."""
        super().__init__(db)

    async def create_student(self, *, new_student: StudentCreate) -> StudentInDb:
        """Create a new student."""
        audit_logger.info("Creating student...", new_student.model_dump())
        created_student = await self.db.fetch_one(
            query=CREATE_STUDENT_QUERY, values=new_student.model_dump()
        )
        audit_logger.info("Student creation completed")
        return StudentInDb(**created_student)

    async def get_student_by_id(self, *, id: UUID) -> StudentInDb:
        """Get a student by their ID."""
        student = await self.db.fetch_one(query=GET_STUDENT_BY_ID_QUERY, values={"id": id})
        if not student:
            raise NotFoundError(entity_name="Student")
        return StudentInDb(**student)

    async def update_student(self, *, id: UUID, student_update: StudentUpdate) -> StudentInDb:
        """Update a student."""
        updated_student = await self.db.fetch_one(
            query=UPDATE_STUDENT_QUERY,
            values={"id": id, **student_update.model_dump()},
        )
        if not updated_student:
            raise NotFoundError(entity_name="Student")
        return StudentInDb(**updated_student)

    async def delete_student(self, *, id: UUID) -> StudentInDb:
        """Delete a student."""
        deleted_student = await self.db.fetch_one(
            query=DELETE_STUDENT_BY_ID_QUERY, values={"id": id}
        )
        if not deleted_student:
            raise NotFoundError(entity_name="Student")
        return StudentInDb(**deleted_student)
