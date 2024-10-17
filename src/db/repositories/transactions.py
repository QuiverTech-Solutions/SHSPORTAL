"""Transaction repository."""

import logging
from typing import Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.errors.database import NotFoundError
from src.models.transactions import TransactionCreate, TransactionInDb, TransactionUpdate

CREATE_TRANSACTION_QUERY = """
INSERT INTO transactions (amount, student_name, school_id, school_name, reference)
VALUES (:amount, :student_name, :school_id, :school_name, :reference)
RETURNING id, amount, student_name, school_id, school_name, reference, created_at, updated_at, is_deleted
"""

GET_TRANSACTION_BY_ID_QUERY = """
SELECT id, amount, student_name, school_id, school_name, reference, created_at, updated_at, is_deleted
FROM transactions
WHERE id = :id AND is_deleted = FALSE
"""

UPDATE_TRANSACTION_QUERY = """
UPDATE transactions
SET amount = :amount, student_name = :student_name, school_id = :school_id, school_name = :school_name, reference = :reference, updated_at = NOW()
WHERE id = :id AND is_deleted = FALSE
RETURNING id, amount, student_name, school_id, school_name, reference, created_at, updated_at, is_deleted
"""

DELETE_TRANSACTION_QUERY = """
UPDATE transactions
SET is_deleted = TRUE
WHERE id = :id AND is_deleted = FALSE
RETURNING id, amount, student_name, school_id, school_name, reference, created_at, updated_at, is_deleted
"""

audit_logger = logging.getLogger("audit")


class TransactionRepository(BaseRepository):
    """Transaction repository."""

    def __init__(self, db: Database) -> None:
        """Constructor for Transaction repository."""
        super().__init__(db)

    async def create_transaction(self, *, new_transaction: TransactionCreate) -> TransactionInDb:
        """Create a new transaction."""
        audit_logger.info("Creating Transaction...", new_transaction.model_dump())
        created_transaction = await self.db.fetch_one(
            query=CREATE_TRANSACTION_QUERY, values=new_transaction.model_dump()
        )
        audit_logger.info("Transaction creation completed")
        return TransactionInDb(**created_transaction)

    async def get_transaction_by_id(self, *, id: UUID) -> TransactionInDb:
        """Get a transaction by ID."""
        transaction = await self.db.fetch_one(query=GET_TRANSACTION_BY_ID_QUERY, values={"id": id})
        if not transaction:
            raise NotFoundError(entity_name="Transaction")
        return TransactionInDb(**transaction)

    async def update_transaction(self, *, id: UUID, transaction_update: TransactionUpdate) -> TransactionInDb:
        """Update a transaction."""
        updated_transaction = await self.db.fetch_one(
            query=UPDATE_TRANSACTION_QUERY,
            values={"id": id, **transaction_update.model_dump()},
        )
        if not updated_transaction:
            raise NotFoundError(entity_name="Transaction")
        return TransactionInDb(**updated_transaction)

    async def delete_transaction(self, *, id: UUID) -> TransactionInDb:
        """Delete a transaction."""
        deleted_transaction = await self.db.fetch_one(
            query=DELETE_TRANSACTION_QUERY, values={"id": id}
        )
        if not deleted_transaction:
            raise NotFoundError(entity_name="Transaction")
        return TransactionInDb(**deleted_transaction)
