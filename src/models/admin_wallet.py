from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class AdminWalletBase(BaseModel):
    """Shared properties for AdminWallet."""
    admin_id: UUID
    provider: str = Field(default="Paystack", max_length=50)
    account_number: str = Field(..., max_length=50)
    balance: float = 0.0


class AdminWalletCreate(AdminWalletBase):
    """Properties to create a new AdminWallet."""
    id: Optional[UUID] = Field(None, description="ID of the wallet")  # Optional in case it's generated at creation.


class AdminWalletUpdate(BaseModel):
    """Properties to update an existing AdminWallet."""
    balance: Optional[float]


class AdminWalletInDb(BaseModel):
    """Properties stored in DB for AdminWallet."""
    id: UUID
    admin_id: UUID
    provider: str = Field(..., max_length=50)
    account_number: str = Field(..., max_length=50)
    balance: float
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False

    class Config:
        orm_mode = True


class AdminWallet(AdminWalletInDb):
    """Properties returned via API for AdminWallet."""
    pass


class AdminWalletPublic(BaseModel):
    """Public properties of an AdminWallet."""
    id: UUID
    admin_id: UUID
    provider: str
    account_number: str
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
