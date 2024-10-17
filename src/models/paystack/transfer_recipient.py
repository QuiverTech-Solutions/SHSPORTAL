"""Paystack transfer recipeint model."""

from datetime import datetime
from typing import Optional

from pydantic import Field

from src.enums.paystack import RecipientTransferCreateType
from src.models.base import CoreModel


class TransferRecipientDataDetails(CoreModel):
    """A model for the transfer recipient details."""

    account_number: str
    account_name: Optional[str]
    bank_code: str
    bank_name: str
    authorization_code: Optional[str]


class TransferRecipientResponseData(CoreModel):
    """A model for the transfer recipient."""

    domain: str
    type: str
    currency: str
    name: str
    details: TransferRecipientDataDetails
    description: Optional[str] = None
    metadata: Optional[dict] = None
    recipient_code: str
    active: bool
    id: int
    integration: int
    createdAt: datetime  # noqa
    updatedAt: datetime  # noqa


class TransferRecipientResponse(CoreModel):
    """A model for the transfer recipient response."""

    status: bool
    message: str
    data: TransferRecipientResponseData


class TransferRecipientCreate(CoreModel):
    """A model for the transfer recipient create data."""

    type: RecipientTransferCreateType
    account_number: str
    bank_code: str
    currency: str = Field("GHS")
    name: str
