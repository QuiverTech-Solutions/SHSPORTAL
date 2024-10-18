"""Models for USSD payment."""

from decimal import Decimal
from uuid import UUID

from src.enums.network_provider import NetworkProvider
from src.models.base import CoreModel


class CreateUSSDPaymentResponse(CoreModel):
    """A model for the response of creating a payment."""

    authorization_url: str
    access_code: str
    reference: str


class CreateVotingUSSDPayment(CoreModel):
    """A model for creating payment."""

    phone_number: str
    school_name: str
    school_id: UUID
    student_name: str
    amount: Decimal
    network_provider: NetworkProvider
