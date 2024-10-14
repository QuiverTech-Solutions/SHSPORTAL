"""Model for paystack."""

from typing import List, Optional

from pydantic import Field, ValidationInfo, field_validator

from src.models.base import CoreModel, IDModelMixin


class CustomField(CoreModel):
    """Custom field for paystack."""

    display_name: str
    variable_name: str
    value: str


class Metadata(CoreModel):
    """Metadata for paystack."""

    custom_fields: List[CustomField]


class CreatePaymentResponse(CoreModel):
    """A model for the response of creating a payment."""

    authorization_url: str
    access_code: str
    reference: str


class CreatePayment(CoreModel):
    """A model for creating payment."""

    telegram_id: int
    email: Optional[str] = Field(None, description="User's email address (optional)")
    telegram_username: Optional[str]
    answers_count: int
    questions_count: int

    @field_validator("telegram_username")
    def name_must_not_be_empty(
        cls,
        v: str,
        info: ValidationInfo,
    ) -> str:
        """Ensure the username is not empty by inserting ID in there."""
        if not v:
            v = info.data["telegram_id"]
        return str(v)


class CreateSubscriptionPlan(CoreModel):
    """A model for creating a subscription plan."""

    telegram_id: int
    email: str = None
    telegram_username: Optional[str]
    payment_plan_id: int

    @field_validator("telegram_username")
    def name_must_not_be_empty(
        cls,
        v: str,
        info: ValidationInfo,
    ) -> str:
        """Ensure the username is not empty by inserting ID in there."""
        if not v:
            v = info.data["telegram_id"]
        return str(v)


class VerifyTransaction(CoreModel):
    """A model for verifying the transaction."""

    status: bool
    message: str
    data: dict


class CustomerData(CoreModel):
    """A model for the customer data."""

    email: str


class SuccessfulTransaction(CoreModel, IDModelMixin):
    """A model for a successful transaction."""

    status: str
    reference: str
    amount: float
    paid_at: str
    currency: str
    created_at: str
    customer: CustomerData
    metadata: Metadata

    @field_validator(
        "amount",
    )
    def divide_amount_by_100(cls, v: float) -> float:
        """Divide the amount by 100."""
        return v / 100
