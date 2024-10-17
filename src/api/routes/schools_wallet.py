"""Routes to manage school wallets."""

from typing import Optional
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.schools_wallet import SchoolWalletRepository
from src.models.schools_wallet import SchoolWalletCreate, SchoolWalletPublic, SchoolWalletUpdate

school_wallet_router = APIRouter()


@school_wallet_router.post(
    "/",
    response_model=SchoolWalletPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_school_wallet(
    new_wallet: SchoolWalletCreate,
    wallet_repo: SchoolWalletRepository = Depends(get_repository(SchoolWalletRepository)),
) -> SchoolWalletPublic:
    """Create a new school wallet."""
    return await wallet_repo.create_school_wallet(new_wallet=new_wallet)


@school_wallet_router.get(
    "/{id}",
    response_model=SchoolWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def get_school_wallet(
    id: UUID,
    wallet_repo: SchoolWalletRepository = Depends(get_repository(SchoolWalletRepository)),
) -> SchoolWalletPublic:
    """Get a school wallet by its ID."""
    return await wallet_repo.get_school_wallet_by_id(id=id)


@school_wallet_router.get(
    "/school/{school_id}",
    response_model=SchoolWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def get_school_wallet_by_school_id(
    school_id: UUID,
    wallet_repo: SchoolWalletRepository = Depends(get_repository(SchoolWalletRepository)),
) -> SchoolWalletPublic:
    """Get a school wallet by its school ID."""
    return await wallet_repo.get_school_wallet_by_school_id(school_id=school_id)


@school_wallet_router.put(
    "/{id}",
    response_model=SchoolWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def update_school_wallet(
    id: UUID,
    wallet_update: SchoolWalletUpdate,
    wallet_repo: SchoolWalletRepository = Depends(get_repository(SchoolWalletRepository)),
) -> SchoolWalletPublic:
    """Update a school wallet."""
    return await wallet_repo.update_school_wallet(id=id, wallet_update=wallet_update)


@school_wallet_router.delete(
    "/{id}",
    response_model=SchoolWalletPublic,
    status_code=status.HTTP_200_OK,
)
async def delete_school_wallet(
    id: UUID,
    wallet_repo: SchoolWalletRepository = Depends(get_repository(SchoolWalletRepository)),
) -> SchoolWalletPublic:
    """Delete a school wallet."""
    return await wallet_repo.delete_school_wallet(id=id)
