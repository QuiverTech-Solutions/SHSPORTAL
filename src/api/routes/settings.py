"""Settings routes."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies.auth import get_super_admin
from src.api.dependencies.database import get_repository
from src.db.repositories.setting import SettingsRepository
from src.models.settings import SettingsCreate, SettingsPublic

settings_router = APIRouter()


@settings_router.post(
    "/admin",
    response_model=SettingsPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_settings(
    settings_create: SettingsCreate,
    settings_repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
    get_super_admin: str = Depends(get_super_admin),
) -> SettingsPublic:
    """Create a new settings."""
    return await settings_repo.create_settings(settings_create)


@settings_router.get(
    "/admin",
    response_model=List[SettingsPublic],
    status_code=status.HTTP_200_OK,
)
async def get_settings(
    settings_repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
    get_super_admin: str = Depends(get_super_admin),
) -> List[SettingsPublic]:
    """Get all settings."""
    return await settings_repo.get_settings()


@settings_router.get(
    "/admin/search",
    response_model=SettingsPublic,
    status_code=status.HTTP_200_OK,
)
async def get_setting(
    id: Optional[UUID] = Query(None, description="The setting's ID"),
    settings_repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
    key: Optional[str] = Query(None, description="The setting's key"),
    get_super_admin: str = Depends(get_super_admin),
) -> SettingsPublic:
    """Get settings by key."""
    if not (id or key):
        raise HTTPException(
            status_code=400,
            detail="Either id or key must be provided.",
        )
    if sum(bool(x) for x in [id, key]) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide exactly one search criteria.",
        )
    return await settings_repo.get_setting(id=id, key=key)


@settings_router.patch(
    "/admin/{key}",
    response_model=SettingsPublic,
    status_code=status.HTTP_200_OK,
)
async def update_setting(
    key: str,
    settings_update: SettingsCreate,
    settings_repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
    get_super_admin: str = Depends(get_super_admin),
) -> SettingsPublic:
    """Update settings by key."""
    return await settings_repo.update_setting(key, settings_update)


@settings_router.delete(
    "/admin/{key}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_setting(
    key: str,
    settings_repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
    get_super_admin: str = Depends(get_super_admin),
) -> None:
    """Delete settings by key."""
    await settings_repo.delete_setting(key)
