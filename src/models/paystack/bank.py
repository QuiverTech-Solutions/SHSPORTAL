"""List of paystack banks."""

from typing import List, Optional

from src.models.base import CoreModel


class BankData(CoreModel):
    """A model for the bank data."""

    name: str
    slug: str
    code: str
    active: bool
    is_deleted: bool
    country: str
    currency: str
    type: str
    id: int


class RetrieveBanksResponse(CoreModel):
    """A model for retrieving banks."""

    status: bool
    message: str
    data: List[BankData]


class BankAccountVerificationData(CoreModel):
    """A model for the bank account verification data."""

    account_number: str
    account_name: str
    bank_id: int


class BankAccountVerificationResponse(CoreModel):
    """A model for the bank account verification response."""

    status: bool
    message: str
    data: Optional[BankAccountVerificationData]
