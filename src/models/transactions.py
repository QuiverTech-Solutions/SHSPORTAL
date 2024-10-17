"""Transaction models"""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class TransactionBase(BaseModel):
    """Transaction base model"""

    amount: UUID = Field(...)
    student_name: str = Field(...)
    school_id: UUID = Field(...)
    school_name: str = Field(...)
    amount: Decimal = Field(..., gt=0)
    reference: str = Field(..., min_length=5, max_length=50)


class TransactionCreate(TransactionBase):
    """Transaction create model"""

    pass


class TransactionUpdate(BaseModel):
    """Transaction update model"""

    amount: Optional[Decimal] = Field(None, gt=0)
    student_name: Optional[str] = Field(None)
    school_id: Optional[UUID] = None
    school_name: Optional[str] = Field(None)
    amount: Optional[Decimal] = Field(None, gt=0)

    class Config:
        """Configurations for the class"""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class TransactionInDb(
    TransactionCreate, IsDeletedModelMixin, IDModelMixin_, DateTimeModelMixin
):
    """Transaction in DB model"""

    pass


class TransactionPublic(TransactionBase, DateTimeModelMixin, IDModelMixin_):
    """Transaction public model"""

    pass
