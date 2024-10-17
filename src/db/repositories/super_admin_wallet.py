"""Super Admin Wallet repository."""

import logging
from typing import Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.super_admin_wallet import SuperAdminWalletCreate, SuperAdminWalletInDb, SuperAdminWalletUpdate

CREATE_SUPER_ADMIN_WALLET_QUERY = """
INSERT INTO super_admin_wallet (user_id, current_balance, total_earned)
VALUES (:user_id, :current_balance, :total_earned)
RETURNING id, user_id, current_balance, total_earned, created_at, updated_at, is_deleted
"""

GET_SUPER_ADMIN_WALLET_BY_USER_ID_QUERY = """
SELECT id, user_id, current_balance, total_earned, created_at, updated_at, is_deleted
FROM super_admin_wallet
WHERE user_id = :user_id AND is_deleted = FALSE
"""

UPDATE_SUPER_ADMIN_WALLET_QUERY = """
UPDATE super_admin_wallet
SET current_balance = :current_balance, total_earned = :total_earned, updated_at = NOW()
WHERE user_id = :user_id AND is_deleted = FALSE
RETURNING id, user_id, current_balance, total_earned, created_at, updated_at, is_deleted
"""

DELETE_SUPER_ADMIN_WALLET_QUERY = """
UPDATE super_admin_wallet
SET is_deleted = TRUE
WHERE user_id = :user_id AND is_deleted = FALSE
RETURNING id, user_id, current_balance, total_earned, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class SuperAdminWalletRepository(BaseRepository):
    """Super Admin Wallet repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for Super Admin Wallet repository."""
        super().__init__(db)

    async def create_super_admin_wallet(self, *, new_wallet: SuperAdminWalletCreate) -> SuperAdminWalletInDb:
        """Create a new Super Admin Wallet."""
        audit_logger.info("Creating Super Admin Wallet...", new_wallet.model_dump())
        created_wallet = await self.db.fetch_one(
            query=CREATE_SUPER_ADMIN_WALLET_QUERY, values=new_wallet.model_dump()
        )
        audit_logger.info("Super Admin Wallet creation completed")
        return SuperAdminWalletInDb(**created_wallet)

    async def get_super_admin_wallet_by_user_id(self, *, user_id: UUID) -> SuperAdminWalletInDb:
        """Get a Super Admin Wallet by user ID."""
        wallet = await self.db.fetch_one(query=GET_SUPER_ADMIN_WALLET_BY_USER_ID_QUERY, values={"user_id": user_id})
        if not wallet:
            raise NotFoundError(entity_name="Super Admin Wallet")
        return SuperAdminWalletInDb(**wallet)

    async def update_super_admin_wallet(self, *, user_id: UUID, wallet_update: SuperAdminWalletUpdate) -> SuperAdminWalletInDb:
        """Update a Super Admin Wallet."""
        updated_wallet = await self.db.fetch_one(
            query=UPDATE_SUPER_ADMIN_WALLET_QUERY,
            values={"user_id": user_id, **wallet_update.model_dump()},
        )
        if not updated_wallet:
            raise NotFoundError(entity_name="Super Admin Wallet")
        return SuperAdminWalletInDb(**updated_wallet)

    async def delete_super_admin_wallet(self, *, user_id: UUID) -> SuperAdminWalletInDb:
        """Delete a Super Admin Wallet."""
        deleted_wallet = await self.db.fetch_one(
            query=DELETE_SUPER_ADMIN_WALLET_QUERY, values={"user_id": user_id}
        )
        if not deleted_wallet:
            raise NotFoundError(entity_name="Super Admin Wallet")
        return SuperAdminWalletInDb(**deleted_wallet)
