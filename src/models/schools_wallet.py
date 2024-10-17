"""Schools wallet model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class SchoolWalletBase(BaseModel):
    """School Wallet base model"""

    school_admin_id: UUID = Field(...)
    school_id: UUID = Field(...)
    current_balance: Decimal = Field(..., ge=0.00)
    total_earned: Decimal = Field(..., ge=0.00)
    last_updated: datetime = Field(...)


class SchoolWalletCreate(SchoolWalletBase):
    """School Wallet create model"""

    pass


class SchoolWalletUpdate(BaseModel):
    """School Wallet update model"""

    current_balance: Optional[Decimal] = Field(None, ge=0.00)
    total_earned: Optional[Decimal] = Field(None, ge=0.00)
    last_updated: Optional[datetime] = None

    class Config:
        """Configurations for the class"""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class SchoolWalletInDb(
    SchoolWalletCreate, IDModelMixin_, DateTimeModelMixin, IsDeletedModelMixin
):
    """School Wallet in DB model"""

    pass


class SchoolWalletPublic(SchoolWalletBase, IDModelMixin_, DateTimeModelMixin):
    """School Wallet public model"""

    pass
