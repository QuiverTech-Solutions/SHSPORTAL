"""Roles Repository"""

from typing import List
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.errors.database import FailedToCreateUpdateQueryError, NotFoundError
from src.models.role import RoleCreate, RoleInDb, RoleUpdate
from src.utils.helpers import Helpers

CREATE_ROLE_QUERY = """
INSERT INTO roles (name)
VALUES (:name)
RETURNING id, name, created_at, updated_at, is_deleted
"""

GET_ROLE_BY_ID_QUERY = """
SELECT id, name, created_at, updated_at,is_deleted
FROM roles
WHERE id = :id
"""

GET_ROLE_BY_NAME_QUERY = """
SELECT id, name, created_at, updated_at,is_deleted
FROM roles
WHERE name = :name
"""

GET_ALL_ROLES_QUERY = """
SELECT id, name, created_at, updated_at,is_deleted
FROM roles
"""

DELETE_ROLE_BY_ID_QUERY = """
DELETE FROM roles
WHERE id = :id
RETURNING id
"""


class RolesRepository(BaseRepository):
    """Roles Repository"""

    def __init__(self, db: Database) -> None:
        """Constructor for Roles Repository"""
        super().__init__(db)

    @handle_post_database_exceptions("Role", already_exists_entity="Role name")
    async def create_role(self, *, new_role: RoleCreate) -> RoleInDb:
        """Create a new role."""
        created_role = await self.db.fetch_one(
            query=CREATE_ROLE_QUERY, values=new_role.model_dump()
        )
        return RoleInDb(**created_role)

    @handle_get_database_exceptions("Role")
    async def get_role(self, *, id: UUID = None, name: str = None) -> RoleInDb:
        """Get a role by id or name."""
        search_criteria = {
            "id": (GET_ROLE_BY_ID_QUERY, id),
            "name": (GET_ROLE_BY_NAME_QUERY, name),
        }

        for field, (query, value) in search_criteria.items():
            if value:
                role = await self.db.fetch_one(query=query, values={field: value})
                if role:
                    return RoleInDb(**role)
                raise NotFoundError(entity_name="Role", entity_identifier=field)
        raise ValueError("At least one of id or name must be provided.")

    @handle_get_database_exceptions("Role")
    async def get_roles(self) -> List[RoleInDb]:
        """Get all roles."""
        roles = await self.db.fetch_all(query=GET_ALL_ROLES_QUERY)
        return [RoleInDb(**role) for role in roles]

    @handle_get_database_exceptions("Role")
    async def update_role(self, *, role_id: UUID, role_update: RoleUpdate) -> RoleInDb:
        """Updates a Role by role id."""
        role_record = await self.get_role(id=role_id)

        update_fields = role_update.model_dump(exclude_unset=True)
        if not update_fields:
            return RoleInDb(**role_record)

        conditions = {"id": role_id}

        # Generate the update query
        UPDATE_ROLE_BY_ID_QUERY = Helpers.generate_update_entity_query(
            table_name="roles",
            update_fields=update_fields,
            conditions=conditions,
        )

        if not UPDATE_ROLE_BY_ID_QUERY:
            raise FailedToCreateUpdateQueryError("Role")

        # Execute the update query
        updated_role = await self.db.fetch_one(
            query=UPDATE_ROLE_BY_ID_QUERY,
            values={**update_fields, "id": role_id},
        )

        if not updated_role:
            raise NotFoundError(entity_name="role", entity_identifier=role_id)

        return RoleInDb(**updated_role)

    @handle_get_database_exceptions("Role")
    async def delete_role(self, *, id: UUID) -> UUID:
        """Delete a role by id."""
        record_id = await self.db.fetch_one(
            query=DELETE_ROLE_BY_ID_QUERY, values={"id": id}
        )
        if record_id:
            return record_id
        raise NotFoundError(entity_name="Role", entity_identifier="id")
