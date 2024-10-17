"""School repository."""

import logging
from typing import Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.schools import SchoolCreate, SchoolInDb, SchoolUpdate

CREATE_SCHOOL_QUERY = """
INSERT INTO schools (name, location, registration_fee)
VALUES (:name, :location, :registration_fee)
RETURNING id, name, location, registration_fee, created_at, updated_at, is_deleted
"""

GET_SCHOOL_BY_ID_QUERY = """
SELECT id, name, location, registration_fee, created_at, updated_at, is_deleted
FROM schools
WHERE id = :id AND is_deleted = FALSE
"""

UPDATE_SCHOOL_QUERY = """
UPDATE schools
SET name = :name, location = :location, registration_fee = :registration_fee, updated_at = NOW()
WHERE id = :id AND is_deleted = FALSE
RETURNING id, name, location, registration_fee, created_at, updated_at, is_deleted
"""

DELETE_SCHOOL_BY_ID_QUERY = """
UPDATE schools
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, name, location, registration_fee, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class SchoolRepository(BaseRepository):
    """School repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for School repository."""
        super().__init__(db)

    async def create_school(self, *, new_school: SchoolCreate) -> SchoolInDb:
        """Create a new school."""
        audit_logger.info("Creating school...", new_school.model_dump())
        created_school = await self.db.fetch_one(
            query=CREATE_SCHOOL_QUERY, values=new_school.model_dump()
        )
        audit_logger.info("School creation completed")

        return SchoolInDb(**created_school)

    async def get_school_by_id(self, *, id: UUID) -> SchoolInDb:
        """Get a school by its ID."""
        school = await self.db.fetch_one(query=GET_SCHOOL_BY_ID_QUERY, values={"id": id})
        if not school:
            raise NotFoundError(entity_name="School")
        return SchoolInDb(**school)

    async def update_school(self, *, id: UUID, school_update: SchoolUpdate) -> SchoolInDb:
        """Update a school."""
        updated_school = await self.db.fetch_one(
            query=UPDATE_SCHOOL_QUERY,
            values={"id": id, **school_update.model_dump()},
        )
        if not updated_school:
            raise NotFoundError(entity_name="School")
        return SchoolInDb(**updated_school)

    async def delete_school(self, *, id: UUID) -> SchoolInDb:
        """Delete a school."""
        deleted_school = await self.db.fetch_one(
            query=DELETE_SCHOOL_BY_ID_QUERY, values={"id": id}
        )
        if not deleted_school:
            raise NotFoundError(entity_name="School")
        return SchoolInDb(**deleted_school)
