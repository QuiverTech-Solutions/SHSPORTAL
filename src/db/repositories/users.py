"""User Repository"""

from typing import List, Optional
from uuid import UUID

from databases import Database
from fastapi.security import OAuth2PasswordRequestForm

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.models.token import AccessToken
from src.models.users import UserCreate, UserInDb, UserUpdate


class UserRepository(BaseRepository):
    """Contains logic for all user operations."""

    def __init__(self, db: Database) -> None:
        """Initializes(gets) DB."""
        super().__init__(db)

    @handle_post_database_exceptions(
        "User", already_exists_entity="Email or referral code"
    )
    async def create_user(self, *, new_user: UserCreate) -> Optional[UserInDb]:
        """Creates a new user."""
        return

    async def login(self, user_request: OAuth2PasswordRequestForm) -> AccessToken:
        """Logs in a user."""
        return

    @handle_get_database_exceptions("User")
    async def get_user(
        self, *, email: str = None, user_id: UUID = None
    ) -> Optional[UserInDb]:
        """Gets a user by email,  phone_number, username, or user_id."""
        return

    @handle_get_database_exceptions("User")
    async def get_users(self) -> List[UserInDb]:
        """Gets all users."""
        return

    @handle_get_database_exceptions("User")
    async def get_total_users(self) -> int:
        """Gets the total number of users."""
        return

    @handle_post_database_exceptions("User", "Role")
    async def update_user_roles(
        self, *, user_id: UUID, new_role: str, type: str = "add"
    ) -> Optional[UserInDb]:
        """Adds a role to the user."""
        return

    @handle_get_database_exceptions("User")
    async def update_user(
        self, *, user_id: UUID, user_update: UserUpdate, is_admin: bool = False
    ) -> Optional[UserInDb]:
        """Updates an user by user_id."""
        return

    @handle_get_database_exceptions("User")
    async def delete_user(self, *, user_id: UUID) -> UUID:
        """Deletes a user by user_id."""
        return
