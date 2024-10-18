from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.admin_wallet import AdminWalletRepository
from src.models.admin_wallet import AdminWalletCreate, AdminWalletPublic, AdminWalletUpdate
from src.models.users import UserInDb

admin_wallet_router = APIRouter()


@admin_wallet_router.post(
    "/", response_model=AdminWalletPublic, status_code=status.HTTP_201_CREATED
)
async def create_admin_wallet(
    new_wallet: AdminWalletCreate,
    wallet_repo: AdminWalletRepository = Depends(get_repository(AdminWalletRepository)),
    current_admin: UserInDb = Depends(get_current_admin),
) -> AdminWalletPublic:
    """Create a new admin wallet."""
    return await wallet_repo.create_wallet(new_wallet=new_wallet)


@admin_wallet_router.get(
    "/", response_model=List[AdminWalletPublic], status_code=status.HTTP_200_OK
)
async def get_all_admin_wallets(
    current_user: UserInDb = Depends(get_current_user),
    wallet_repo: AdminWalletRepository = Depends(get_repository(AdminWalletRepository)),
) -> List[AdminWalletPublic]:
    """Get all admin wallets."""
    return await wallet_repo.get_wallets()


@admin_wallet_router.get(
    "/search", response_model=AdminWalletPublic, status_code=status.HTTP_200_OK
)
async def get_admin_wallet(
    id: Optional[UUID] = Query(None, description="The admin wallet's ID"),
    account_number: Optional[str] = Query(None, description="The admin wallet's account number"),
    wallet_repo: AdminWalletRepository = Depends(get_repository(AdminWalletRepository)),
    current_user: UserInDb = Depends(get_current_user),
) -> AdminWalletPublic:
    """Get an admin wallet by ID or account number."""
    if not (id or account_number):
        raise HTTPException(
            status_code=400,
            detail="Either the wallet's ID or account number must be provided.",
        )
    if sum(bool(x) for x in [id, account_number]) > 1:
        raise HTTPException(
            status_code=400,
            detail="Only one of the wallet's ID or account number can be provided at a time.",
        )
    return await wallet_repo.get_wallet(id=id, account_number=account_number)


@admin_wallet_router.put(
    "/{wallet_id}/balance", response_model=AdminWalletPublic, status_code=status.HTTP_200_OK
)
async def update_admin_wallet_balance(
    wallet_id: UUID,
    balance_update: AdminWalletUpdate,
    wallet_repo: AdminWalletRepository = Depends(get_repository(AdminWalletRepository)),
    current_admin: UserInDb = Depends(get_current_admin),
) -> AdminWalletPublic:
    """Update an admin wallet's balance."""
    updated_wallet = await wallet_repo.update_wallet_balance(wallet_id=wallet_id, new_balance=balance_update.balance)
    if not updated_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found.")
    return updated_wallet


@admin_wallet_router.delete("/{wallet_id}", status_code=status.HTTP_200_OK)
async def delete_admin_wallet(
    wallet_id: UUID,
    wallet_repo: AdminWalletRepository = Depends(get_repository(AdminWalletRepository)),
    current_admin: UserInDb = Depends(get_current_admin),
) -> UUID:
    """Delete an admin wallet."""
    deleted_wallet = await wallet_repo.delete_wallet(wallet_id=wallet_id)
    if not deleted_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found.")
    return wallet_id
