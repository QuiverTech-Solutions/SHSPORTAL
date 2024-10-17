"""Refresh RefreshTokenInDb repository."""

from typing import Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.models.refresh_token import RefreshTokenCreate, RefreshTokenInDb

CREATE_REFRESH_TOKEN_QUERY = """
INSERT INTO refresh_tokens (token, user_id, is_active)
VALUES (:token, :user_id, :is_active)
RETURNING  id, token, user_id, is_active, is_deleted, created_at, updated_at
"""

GET_ACTIVE_REFRESH_TOKEN_BY_USER_ID_QUERY = """
SELECT id, token, user_id, is_active, is_deleted, created_at, updated_at
FROM refresh_tokens
WHERE user_id = :user_id AND is_active = TRUE AND is_deleted = FALSE
"""

GET_ALL_REFRESH_TOKENS_BY_USER_ID_QUERY = """
SELECT id, token, user_id, is_active, is_deleted, created_at, updated_at
FROM refresh_tokens
WHERE user_id = :user_id AND is_deleted = FALSE
"""

GET_REFRESH_TOKEN_BY_ID_QUERY = """
SELECT id, token, user_id, is_active, is_deleted, created_at, updated_at
FROM refresh_tokens
WHERE id = :id AND is_deleted = FALSE
"""

DEACTIVATE_ACTIVE_REFRESH_TOKEN_FOR_USER_QUERY = """
UPDATE refresh_tokens
SET is_active = FALSE
WHERE user_id = :user_id AND is_active = TRUE AND is_deleted = FALSE"""

DEACTIVATE_REFRESH_TOKEN_BY_ID_QUERY = """
UPDATE refresh_tokens
SET is_active = FALSE
WHERE id = :id AND is_active = TRUE AND is_deleted = FALSE
RETURNING id
"""


class RefreshTokenRepository(BaseRepository):
    """Contains logic for all refresh RefreshTokenInDb operations."""

    def __init__(self, db: Database) -> None:
        """Initializes(gets) DB."""
        super().__init__(db)

    @handle_post_database_exceptions("refresh token", "User id", "Refresh Token")
    async def create_refresh_token(
        self, *, new_token: RefreshTokenCreate
    ) -> RefreshTokenInDb:
        """Create a new refresh token."""
        created_token = await self.db.fetch_one(
            query=CREATE_REFRESH_TOKEN_QUERY,
            values={**new_token.model_dump()},
        )
        return RefreshTokenInDb(**dict(created_token))

    @handle_get_database_exceptions("Refresh token")
    async def get_active_refresh_token_by_user_id(
        self, *, user_id: UUID
    ) -> Optional[RefreshTokenInDb]:
        """Get active refresh token by user id."""
        token_record = await self.db.fetch_one(
            query=GET_ACTIVE_REFRESH_TOKEN_BY_USER_ID_QUERY,
            values={"user_id": user_id},
        )
        if token_record:
            return RefreshTokenInDb(**dict(token_record))

    @handle_get_database_exceptions("Refresh token")
    async def get_all_refresh_tokens_by_user_id(
        self, *, user_id: UUID
    ) -> list[RefreshTokenInDb]:
        """Get all refresh tokens by user id."""
        token_records = await self.db.fetch_all(
            query=GET_ALL_REFRESH_TOKENS_BY_USER_ID_QUERY,
            values={"user_id": user_id},
        )
        return [
            RefreshTokenInDb(**dict(refresh_token)) for refresh_token in token_records
        ]

    @handle_get_database_exceptions("Refresh token")
    async def get_refresh_token_by_id(
        self, *, token_id: UUID
    ) -> Optional[RefreshTokenInDb]:
        """Get refresh token by id."""
        token_record = await self.db.fetch_one(
            query=GET_REFRESH_TOKEN_BY_ID_QUERY, values={"id": token_id}
        )
        if token_record:
            return RefreshTokenInDb(**dict(token_record))

    @handle_get_database_exceptions("Refresh token")
    async def deactivate_refresh_token_by_id(self, *, token_id: UUID) -> None:
        """Deactivate refresh token by id."""
        await self.db.fetch_one(
            query=DEACTIVATE_REFRESH_TOKEN_BY_ID_QUERY, values={"id": token_id}
        )

    @handle_get_database_exceptions("refresh token")
    async def deactivate_active_refresh_token_for_user(self, *, user_id: UUID) -> None:
        """Deactivate active refresh token for user."""
        await self.db.fetch_one(
            query=DEACTIVATE_ACTIVE_REFRESH_TOKEN_FOR_USER_QUERY,
            values={"user_id": user_id},
        )
