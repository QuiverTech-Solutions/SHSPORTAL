"""This module contains the models for the charge(ussd) endpoint."""

from typing import Optional

from src.models.base import CoreModel


class ChargeResponseData(CoreModel):
    """A model for the charge response data."""

    reference: str
    status: str
    display_text: Optional[str] = None


class ChargeResponse(CoreModel):
    """A model for the charge response."""

    status: bool
    message: str
    data: Optional[ChargeResponseData] = None


class ChargeOTPVerifyRequest(CoreModel):
    """A model for the charge otp verify request."""

    otp: str
    reference: str
