"""Schools model."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class SchoolBase(BaseModel):
    """School base model"""

    name: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)
    registration_fee: float = Field(..., gt=0)
    updated_at: Optional[datetime]  # This field can be auto-updated on each update operation


class SchoolCreate(SchoolBase):
    """School create model"""
    
    pass


class SchoolUpdate(BaseModel):
    """School update model"""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    registration_fee: Optional[float] = Field(None, gt=0)
    updated_at: datetime = Field(default_factory=datetime.now)  # Set updated_at during updates

    class Config:
        """Configurations for the class."""
        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class SchoolInDb(SchoolCreate, IsDeletedModelMixin, IDModelMixin_, DateTimeModelMixin):
    """School in DB model"""
    
    updated_at: datetime  # Ensure this is stored in the database


class SchoolPublic(SchoolBase, DateTimeModelMixin, IDModelMixin_):
    """School public model"""

    updated_at: datetime  # Expose this field in the public response
