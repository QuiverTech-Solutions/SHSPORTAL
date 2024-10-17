import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.transactions import TransactionRepository
from src.models.transactions import TransactionCreate, TransactionPublic, TransactionUpdate

transaction_router = APIRouter()
audit_logger = logging.getLogger("audit")


@transaction_router.post(
    "/transactions",
    response_model=TransactionPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    transaction_create: TransactionCreate,
    transaction_repo: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionPublic:
    """Create a new transaction."""
    return await transaction_repo.create_transaction(new_transaction=transaction_create)


@transaction_router.get(
    "/transactions/{id}",
    response_model=TransactionPublic,
    status_code=status.HTTP_200_OK,
)
async def get_transaction(
    id: UUID,
    transaction_repo: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionPublic:
    """Get a transaction by ID."""
    return await transaction_repo.get_transaction_by_id(id=id)


@transaction_router.put(
    "/transactions/{id}",
    response_model=TransactionPublic,
    status_code=status.HTTP_200_OK,
)
async def update_transaction(
    id: UUID,
    transaction_update: TransactionUpdate,
    transaction_repo: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionPublic:
    """Update a transaction."""
    return await transaction_repo.update_transaction(id=id, transaction_update=transaction_update)


@transaction_router.delete(
    "/transactions/{id}",
    response_model=TransactionPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_transaction(
    id: UUID,
    transaction_repo: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionPublic:
    """Delete a transaction."""
    return await transaction_repo.delete_transaction(id=id)
