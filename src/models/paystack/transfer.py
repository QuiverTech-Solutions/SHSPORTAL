"""Paystack model for transfer request."""

from decimal import Decimal
from pydantic import field_validator

from src.models.base import CoreModel


class TransferRequest(CoreModel):
    """A model for withdrawing funds."""

    amount: Decimal
    reason: str


class TransferResponseData(CoreModel):
    """A model for the transfer response data."""

    reference: str
    integration: int
    domain: str
    amount: Decimal
    currency: str
    source: str
    reason: str
    recipient: int
    status: str
    transfer_code: str
    id: int
    createdAt: str  # noqa
    updatedAt: str  # noqa


class TransferResponse(CoreModel):
    """A model for the transfer response."""

    status: bool
    message: str
    data: TransferResponseData


class TransferWebhookData(CoreModel):
    """A model for the transfer webhook data."""

    amount: Decimal
    currency: str
    domain: str
    id: int
    reason: str
    reference: str
    source: str
    status: str
    transfer_code: str

    @field_validator(
        "amount",
    )
    def divide_amount_by_100(cls, v: Decimal) -> Decimal:
        """Divide the amount by 100."""
        return v / 100


class TransferSuccessEvent(CoreModel):
    """A model for the transfer success event."""

    event: str
    data: TransferWebhookData
