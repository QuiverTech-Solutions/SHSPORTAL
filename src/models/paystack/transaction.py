"""Paystack transaction model."""

from decimal import Decimal
from pydantic import field_validator

from src.models.base import CoreModel


class CustomerData(CoreModel):
    """A model for the customer data."""

    email: str


class CustomField(CoreModel):
    """Custom field for paystack."""

    display_name: str
    variable_name: str
    value: str


class Metadata(CoreModel):
    """Metadata for paystack."""

    custom_fields: list[CustomField]


class Authorization(CoreModel):
    """A model for the authorization data."""

    authorization_code: str
    mobile_money_number: str
    channel: str
    account_name: str


class SuccessfulTransaction(CoreModel):
    """A model for a successful transaction."""

    id: int
    status: str
    reference: str
    amount: Decimal
    paid_at: str
    currency: str
    created_at: str
    customer: CustomerData
    metadata: Metadata

    @field_validator(
        "amount",
    )
    def divide_amount_by_100(cls, v: Decimal) -> Decimal:
        """Divide the amount by 100."""
        return v / 100
