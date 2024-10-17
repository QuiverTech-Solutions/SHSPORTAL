import logging
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.super_admin_wallet import SuperAdminWalletRepository
from src.models.super_admin_wallet import SuperAdminWalletCreate, SuperAdminWalletPublic, SuperAdminWalletUpdate

super_admin_wallet_router = APIRouter()
audit_logger = logging.getLogger("audit")


@super_admin_wallet_router.post(
    "/wallet",
    response_model=SuperAdminWalletPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_super_admin_wallet(
    super_admin_wallet_create: SuperAdminWalletCreate,
    wallet_repo: SuperAdminWalletRepository = Depends(get_repository(SuperAdminWalletRepository)),
) -> SuperAdminWalletPublic:
    """Create a new Super Admin Wallet."""
    return await wallet_repo.create_super_admin_wallet(new_wallet=super_admin_wallet_create)


@super_admin_wallet_router.get(
    "/wallet/{user_id}",
    response_model=SuperAdminWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def get_super_admin_wallet(
    user_id: UUID,
    wallet_repo: SuperAdminWalletRepository = Depends(get_repository(SuperAdminWalletRepository)),
) -> SuperAdminWalletPublic:
    """Get a Super Admin Wallet by user ID."""
    return await wallet_repo.get_super_admin_wallet_by_user_id(user_id=user_id)


@super_admin_wallet_router.put(
    "/wallet/{user_id}",
    response_model=SuperAdminWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def update_super_admin_wallet(
    user_id: UUID,
    wallet_update: SuperAdminWalletUpdate,
    wallet_repo: SuperAdminWalletRepository = Depends(get_repository(SuperAdminWalletRepository)),
) -> SuperAdminWalletPublic:
    """Update a Super Admin Wallet."""
    return await wallet_repo.update_super_admin_wallet(user_id=user_id, wallet_update=wallet_update)


@super_admin_wallet_router.delete(
    "/wallet/{user_id}",
    response_model=SuperAdminWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_super_admin_wallet(
    user_id: UUID,
    wallet_repo: SuperAdminWalletRepository = Depends(get_repository(SuperAdminWalletRepository)),
) -> SuperAdminWalletPublic:
    """Delete a Super Admin Wallet."""
    return await wallet_repo.delete_super_admin_wallet(user_id=user_id)
