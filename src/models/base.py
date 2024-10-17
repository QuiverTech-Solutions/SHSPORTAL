"""Core data that exist in all Models."""

# Standard library imports
from datetime import datetime
from typing import Optional
from uuid import UUID

# Third party imports
from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """Any common logic to be shared by all models."""

    pass


class IDModelMixin(BaseModel):
    """ID data."""

    id: int


class DateTimeModelMixin(BaseModel):
    """Datetime model dates."""

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:  # noqa
        """Validate both created_at and update_at data."""
        return value or datetime.now()

    def model_dump(self, *args: tuple, **kwargs: dict) -> dict:
        """Dump model data."""
        d = super().model_dump(*args, **kwargs)
        for field in ["created_at", "updated_at"]:
            if d[field]:
                d[field] = d[field].isoformat()
        return d


class IDModelMixin_(BaseModel):
    """ID data."""

    id: UUID


class UserIDModelMixin(BaseModel):
    """User ID data."""

    user_id: UUID


class IsDeletedModelMixin(BaseModel):
    """Is deleted data."""

    is_deleted: bool = False
