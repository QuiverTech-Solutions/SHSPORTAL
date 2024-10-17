"""School wallet repository."""

import logging
from typing import Optional
from uuid import UUID
from decimal import Decimal

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.schools_wallet import SchoolWalletCreate, SchoolWalletInDb, SchoolWalletUpdate

CREATE_SCHOOL_WALLET_QUERY = """
INSERT INTO school_wallets (school_admin_id, school_id, current_balance, total_earned, last_updated)
VALUES (:school_admin_id, :school_id, :current_balance, :total_earned, :last_updated)
RETURNING id, school_admin_id, school_id, current_balance, total_earned, last_updated, created_at, updated_at, is_deleted
"""

GET_SCHOOL_WALLET_BY_ID_QUERY = """
SELECT id, school_admin_id, school_id, current_balance, total_earned, last_updated, created_at, updated_at, is_deleted
FROM school_wallets
WHERE id = :id AND is_deleted = FALSE
"""

GET_SCHOOL_WALLET_BY_SCHOOL_ID_QUERY = """
SELECT id, school_admin_id, school_id, current_balance, total_earned, last_updated, created_at, updated_at, is_deleted
FROM school_wallets
WHERE school_id = :school_id AND is_deleted = FALSE
"""

UPDATE_SCHOOL_WALLET_QUERY = """
UPDATE school_wallets
SET current_balance = :current_balance, total_earned = :total_earned, last_updated = :last_updated, updated_at = NOW()
WHERE id = :id AND is_deleted = FALSE
RETURNING id, school_admin_id, school_id, current_balance, total_earned, last_updated, created_at, updated_at, is_deleted
"""

DELETE_SCHOOL_WALLET_BY_ID_QUERY = """
UPDATE school_wallets
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, school_admin_id, school_id, current_balance, total_earned, last_updated, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class SchoolWalletRepository(BaseRepository):
    """School wallet repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for School Wallet repository."""
        super().__init__(db)

    async def create_school_wallet(self, *, new_wallet: SchoolWalletCreate) -> SchoolWalletInDb:
        """Create a new school wallet."""
        audit_logger.info("Creating school wallet...", new_wallet.model_dump())
        created_wallet = await self.db.fetch_one(
            query=CREATE_SCHOOL_WALLET_QUERY, values=new_wallet.model_dump()
        )
        audit_logger.info("School wallet creation completed")

        return SchoolWalletInDb(**created_wallet)

    async def get_school_wallet_by_id(self, *, id: UUID) -> SchoolWalletInDb:
        """Get a school wallet by its ID."""
        wallet = await self.db.fetch_one(query=GET_SCHOOL_WALLET_BY_ID_QUERY, values={"id": id})
        if not wallet:
            raise NotFoundError(entity_name="School Wallet")
        return SchoolWalletInDb(**wallet)

    async def get_school_wallet_by_school_id(self, *, school_id: UUID) -> SchoolWalletInDb:
        """Get a school wallet by its school ID."""
        wallet = await self.db.fetch_one(
            query=GET_SCHOOL_WALLET_BY_SCHOOL_ID_QUERY, values={"school_id": school_id}
        )
        if not wallet:
            raise NotFoundError(entity_name="School Wallet")
        return SchoolWalletInDb(**wallet)

    async def update_school_wallet(
        self, *, id: UUID, wallet_update: SchoolWalletUpdate
    ) -> SchoolWalletInDb:
        """Update a school wallet."""
        updated_wallet = await self.db.fetch_one(
            query=UPDATE_SCHOOL_WALLET_QUERY,
            values={"id": id, **wallet_update.model_dump()},
        )
        if not updated_wallet:
            raise NotFoundError(entity_name="School Wallet")
        return SchoolWalletInDb(**updated_wallet)

    async def delete_school_wallet(self, *, id: UUID) -> SchoolWalletInDb:
        """Delete a school wallet."""
        deleted_wallet = await self.db.fetch_one(
            query=DELETE_SCHOOL_WALLET_BY_ID_QUERY, values={"id": id}
        )
        if not deleted_wallet:
            raise NotFoundError(entity_name="School Wallet")
        return SchoolWalletInDb(**deleted_wallet)
