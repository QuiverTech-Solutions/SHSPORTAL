"""Admin Wallet Repository."""

from typing import List
from databases import Database
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.db.repositories.base import BaseRepository
from src.errors.core import InternalServerError
from src.errors.database import AlreadyExistsError, NotFoundError
from src.models.admin_wallet import AdminWalletCreate, AdminWalletInDb

CREATE_ADMIN_WALLET_QUERY = """
INSERT INTO admin_wallets (id, admin_id, provider, account_number, balance)
VALUES (:id, :admin_id, :provider, :account_number, :balance)
RETURNING id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
"""

GET_ADMIN_WALLET_BY_ID_QUERY = """
SELECT id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
FROM admin_wallets
WHERE id = :id AND is_deleted = FALSE
"""

GET_ADMIN_WALLET_BY_ACCOUNT_NUMBER_QUERY = """
SELECT id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
FROM admin_wallets
WHERE account_number = :account_number AND is_deleted = FALSE
"""

GET_ALL_ADMIN_WALLETS = """
SELECT id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
FROM admin_wallets
WHERE is_deleted = FALSE
"""

UPDATE_ADMIN_WALLET_BALANCE_QUERY = """
UPDATE admin_wallets
SET balance = :balance
WHERE id = :id AND is_deleted = FALSE
RETURNING id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
"""

DELETE_ADMIN_WALLET_QUERY = """
UPDATE admin_wallets
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, admin_id, provider, account_number, balance, created_at, updated_at, is_deleted
"""

class AdminWalletRepository(BaseRepository):
    """Admin Wallet Repository."""

    def __init__(self, db: Database) -> None:
        """Initialize Admin Wallet Repository."""
        super().__init__(db)

    async def create_wallet(self, *, new_wallet: AdminWalletCreate) -> AdminWalletInDb:
        """Create a new admin wallet."""
        try:
            created_wallet = await self.db.fetch_one(
                query=CREATE_ADMIN_WALLET_QUERY, values=new_wallet.model_dump()
            )
            return AdminWalletInDb(**created_wallet)
        except IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                raise AlreadyExistsError(entity_name="Admin Wallet") from e
            raise InternalServerError("Failed to create admin wallet.") from e
        except SQLAlchemyError as e:
            raise InternalServerError("Failed to create admin wallet due to a database error.") from e

    async def get_wallet(self, *, id: str = None, account_number: str = None) -> AdminWalletInDb:
        """Get an admin wallet."""
        search_criteria = {
            "id": (GET_ADMIN_WALLET_BY_ID_QUERY, id),
            "account_number": (GET_ADMIN_WALLET_BY_ACCOUNT_NUMBER_QUERY, account_number),
        }
        for field, (query, value) in search_criteria.items():
            if value:
                wallet = await self.db.fetch_one(query=query, values={field: value})
                if wallet:
                    return AdminWalletInDb(**wallet)
                else:
                    raise NotFoundError(entity_name="Admin Wallet", entity_identifier=field)
        raise ValueError("No valid arguments provided to get admin wallet.")

    async def get_wallets(self) -> List[AdminWalletInDb]:
        """Get all admin wallets."""
        wallets = await self.db.fetch_all(query=GET_ALL_ADMIN_WALLETS)
        return [AdminWalletInDb(**wallet) for wallet in wallets]

    async def update_wallet_balance(self, *, wallet_id: str, new_balance: float) -> AdminWalletInDb:
        """Update an admin wallet's balance."""
        updated_wallet = await self.db.fetch_one(
            query=UPDATE_ADMIN_WALLET_BALANCE_QUERY, values={"id": wallet_id, "balance": new_balance}
        )
        if updated_wallet is None:
            raise NotFoundError(entity_name="Admin Wallet", entity_identifier="id")
        return AdminWalletInDb(**updated_wallet)

    async def delete_wallet(self, *, wallet_id: str) -> AdminWalletInDb:
        """Delete an admin wallet."""
        deleted_wallet = await self.db.fetch_one(query=DELETE_ADMIN_WALLET_QUERY, values={"id": wallet_id})
        if deleted_wallet is None:
            raise NotFoundError(detail="Admin Wallet not found.")
        return AdminWalletInDb(**deleted_wallet)
