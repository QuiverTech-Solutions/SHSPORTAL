"""Students model."""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class StudentBase(BaseModel):
    """Student base model"""

    index_number: str = Field(..., min_length=5, max_length=20)
    name: str = Field(..., min_length=2, max_length=100)
    dob: date = Field(...)
    school_id: UUID = Field(...)
    location: str = Field(..., min_length=2, max_length=100)
    registration_paid: bool = Field(default=False)


class StudentCreate(StudentBase):
    """Student create model"""

    pass


class StudentUpdate(BaseModel):
    """Student update model"""

    index_number: Optional[str] = Field(None, min_length=5, max_length=20)
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    dob: Optional[date] = None
    school_id: Optional[UUID] = None
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    registration_paid: Optional[bool] = None

    class Config:
        """Configurations for the class"""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class StudentInDb(
    StudentCreate, IsDeletedModelMixin, IDModelMixin_, DateTimeModelMixin
):
    """Student in DB model"""

    pass


class StudentPublic(StudentBase, DateTimeModelMixin, IDModelMixin_):
    """Student public model"""

    pass
