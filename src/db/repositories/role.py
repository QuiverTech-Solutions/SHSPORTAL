"""Role repository."""

import logging
from typing import List, Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.role import RoleCreate, RoleInDb, RoleUpdate

CREATE_ROLE_QUERY = """
INSERT INTO roles (name)
VALUES (:name)
RETURNING id, name, created_at, updated_at, is_deleted
"""

GET_ROLE_BY_ID_QUERY = """
SELECT id, name, created_at, updated_at, is_deleted
FROM roles
WHERE id = :id AND is_deleted = FALSE
"""

GET_ROLES_QUERY = """
SELECT id, name, created_at, updated_at, is_deleted
FROM roles
WHERE is_deleted = FALSE
ORDER BY created_at DESC
"""

UPDATE_ROLE_QUERY = """
UPDATE roles
SET name = :name, updated_at = NOW()
WHERE id = :id AND is_deleted = FALSE
RETURNING id, name, created_at, updated_at, is_deleted
"""

DELETE_ROLE_BY_ID_QUERY = """
UPDATE roles
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, name, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class RoleRepository(BaseRepository):
    """Role repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for Role repository."""
        super().__init__(db)

    async def create_role(self, *, new_role: RoleCreate) -> RoleInDb:
        """Create a new role."""
        audit_logger.info("Adding role...", new_role.model_dump())
        created_role = await self.db.fetch_one(
            query=CREATE_ROLE_QUERY, values=new_role.model_dump()
        )
        audit_logger.info("Role creation completed")

        return RoleInDb(**created_role)

    async def get_role(self, *, id: UUID) -> RoleInDb:
        """Get role by id."""
        role = await self.db.fetch_one(query=GET_ROLE_BY_ID_QUERY, values={"id": id})
        if not role:
            raise NotFoundError(entity_name="Role")
        return RoleInDb(**role)

    async def get_roles(self) -> List[RoleInDb]:
        """Get all roles."""
        roles = await self.db.fetch_all(query=GET_ROLES_QUERY)
        return [RoleInDb(**role) for role in roles]

    async def update_role(self, *, id: UUID, role_update: RoleUpdate) -> RoleInDb:
        """Update a role."""
        updated_role = await self.db.fetch_one(
            query=UPDATE_ROLE_QUERY, values={"id": id, **role_update.model_dump()}
        )
        if not updated_role:
            raise NotFoundError(entity_name="Role")
        return RoleInDb(**updated_role)

    async def delete_role(self, *, id: UUID) -> RoleInDb:
        """Delete a role by its id."""
        deleted_role = await self.db.fetch_one(
            query=DELETE_ROLE_BY_ID_QUERY, values={"id": id}
        )
        if not deleted_role:
            raise NotFoundError(entity_name="Role")
        return RoleInDb(**deleted_role)
