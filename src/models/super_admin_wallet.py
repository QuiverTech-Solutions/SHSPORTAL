"""Super admin wallet."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class SuperAdminWalletBase(BaseModel):
    """SuperAdmin Wallet base model"""

    user_id: UUID = Field(...)
    current_balance: Decimal = Field(..., ge=0.00)
    total_earned: Decimal = Field(..., ge=0.00)


class SuperAdminWalletCreate(SuperAdminWalletBase):
    """SuperAdmin Wallet create model"""

    pass


class SuperAdminWalletUpdate(BaseModel):
    """SuperAdmin Wallet update model"""

    current_balance: Optional[Decimal] = Field(None, ge=0.00)
    total_earned: Optional[Decimal] = Field(None, ge=0.00)

    class Config:
        """Configurations for the class"""

        validate_assignment = True
        extra = "forbid"


class SuperAdminWalletInDb(
    SuperAdminWalletCreate, IDModelMixin_, DateTimeModelMixin, IsDeletedModelMixin
):
    """SuperAdmin Wallet in DB model"""

    pass


class SuperAdminWalletPublic(SuperAdminWalletBase, IDModelMixin_, DateTimeModelMixin):
    """SuperAdmin Wallet public model"""

    pass
