from typing import List, Optional
from pydantic import Field, ValidationInfo, field_validator
from src.models.base import CoreModel, IDModelMixin


class CustomField(CoreModel):
    """Custom field for Paystack (used in metadata)."""
    
    display_name: str
    variable_name: str
    value: str


class Metadata(CoreModel):
    """Metadata for Paystack."""
    
    custom_fields: List[CustomField]


class CreatePaymentResponse(CoreModel):
    """Model for the response of creating a payment."""
    
    authorization_url: str
    access_code: str
    reference: str


class CreatePayment(CoreModel):
    """Model for creating a payment."""
    
    student_id: int
    email: Optional[str] = Field(None, description="Student's email address (optional)")
    name: Optional[str]
    application_fee: float
    application_year: int

    @field_validator("name")
    def name_must_not_be_empty(
        cls,
        v: str,
        info: ValidationInfo,
    ) -> str:
        """Ensure the name is not empty by inserting student ID in there."""
        if not v:
            v = info.data["student_id"]
        return str(v)



class VerifyTransaction(CoreModel):
    """Model for verifying a transaction."""
    
    status: bool
    message: str
    data: dict


class CustomerData(CoreModel):
    """Model for customer data (used in successful transactions)."""
    
    email: str


class SuccessfulTransaction(CoreModel, IDModelMixin):
    """Model for a successful transaction."""
    
    status: str
    reference: str
    amount: float
    paid_at: str
    currency: str
    created_at: str
    customer: CustomerData
    metadata: Metadata

    @field_validator("amount")
    def divide_amount_by_100(cls, v: float) -> float:
        """Divide the amount by 100 (Paystack returns amounts in kobo)."""
        return v / 100
