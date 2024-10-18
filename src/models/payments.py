"""Payments model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_


class PaymentBase(BaseModel):
    """Payment base model"""

    student_id: UUID = Field(...)
    school_id: UUID = Field(...)
    total_amount: Decimal = Field(..., gt=0)  # Total payment amount
    school_amount: Decimal = Field(..., gt=0)  # 80% amount to school
    admin_amount: Decimal = Field(..., gt=0)  # 20% amount to admin
    payment_status: str = Field(
        ...
    )  # TODO: Update to Enum with options ['pending', 'completed', 'failed']
    payment_method: str = Field(
        ..., min_length=2, max_length=50
    )  # e.g., 'momo', 'bank'
    transaction_reference: str = Field(..., min_length=5, max_length=100)
    paid_at: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    """Payment create model"""

    pass


class PaymentUpdate(BaseModel):
    """Payment update model"""

    payment_status: Optional[str] = Field(None)
    payment_method: Optional[str] = Field(None, min_length=2, max_length=50)
    transaction_reference: Optional[str] = Field(None, min_length=5, max_length=100)
    paid_at: Optional[datetime] = None

    class Config:
        """Configurations for the class"""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class PaymentInDb(PaymentCreate, IDModelMixin_, DateTimeModelMixin):
    """Payment in DB model"""

    pass


class PaymentPublic(PaymentBase, DateTimeModelMixin, IDModelMixin_):
    """Payment public model"""

    pass
