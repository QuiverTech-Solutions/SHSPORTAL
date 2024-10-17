"""User Role Repository"""

from typing import List
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.db.repositories.role import RolesRepository
from src.db.repositories.user import UserRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.models.user_role import UserRolesCreate, UserRolesInDb

CREATE_USER_ROLE_QUERY = """
INSERT INTO user_roles (user_id, role_id)
VALUES (:user_id, :role_id)
RETURNING user_id, role_id, created_at, updated_at, is_deleted
"""

GET_USER_ROLE_BY_USER_ID_QUERY = """
SELECT user_id, role_id, created_at, updated_at, is_deleted
FROM user_roles
WHERE user_id = :user_id AND is_deleted = FALSE
"""

GET_USER_ROLE_BY_ROLE_ID_QUERY = """
SELECT user_id, role_id, created_at, updated_at, is_deleted
FROM user_roles
WHERE role_id = :role_id AND is_deleted = FALSE
"""

GET_ALL_USER_ROLES_QUERY = """
SELECT user_id, role_id, created_at, updated_at, is_deleted
FROM user_roles
WHERE is_deleted = FALSE
"""

DELETE_USER_ROLE_BY_ROLE_ID_AND_USER_ID = """
DELETE FROM user_roles
WHERE role_id = :role_id AND user_id = :user_id
RETURNING user_id
"""


class UserRoleRepository(BaseRepository):
    """User Role Repository"""

    def __init__(self, db: Database) -> None:
        """Constructor for User Role Repository"""
        super().__init__(db)
        self.roles_repo = RolesRepository(db)
        self.user_repository = UserRepository(db)

    @handle_post_database_exceptions(
        "User Role", "User id and role  id", "User id and role id"
    )
    async def assign_role_to_user(
        self, *, new_user_role: UserRolesCreate
    ) -> UserRolesInDb:
        """Assign a role to the user."""
        async with self.db.transaction():
            role = await self.roles_repo.get_role(name=new_user_role.role_name)
            new_user_role = new_user_role.model_dump(exclude={"role_name"})
            new_user_role["role_id"] = str(role.id)

            user_role = await self.db.fetch_one(
                query=CREATE_USER_ROLE_QUERY, values=new_user_role
            )
            await self.user_repository.update_user_roles(
                user_id=new_user_role["user_id"], new_role=role.name
            )
            return UserRolesInDb(**user_role)

    @handle_get_database_exceptions("User Role")
    async def get_user_roles(
        self, *, role_id: UUID = None, user_id: UUID = None
    ) -> List[UserRolesInDb]:
        """Get a user role by role_id, or user id."""
        search_criteria = {
            "role_id": (GET_USER_ROLE_BY_ROLE_ID_QUERY, role_id),
            "user_id": (GET_USER_ROLE_BY_USER_ID_QUERY, user_id),
        }

        for field, (query, value) in search_criteria.items():
            if value:
                user_roles = await self.db.fetch_all(query=query, values={field: value})
                return [UserRolesInDb(**user_role) for user_role in user_roles]

        user_roles = await self.db.fetch_all(query=GET_ALL_USER_ROLES_QUERY)
        return [UserRolesInDb(**user_role) for user_role in user_roles]

    @handle_get_database_exceptions("User Role")
    async def delete_user_role(self, *, role_id: UUID, user_id: UUID) -> UUID:
        """Delete a user role by role_id and user_id."""
        return await self.db.fetch_val(
            query=DELETE_USER_ROLE_BY_ROLE_ID_AND_USER_ID,
            values={"role_id": role_id, "user_id": user_id},
        )
