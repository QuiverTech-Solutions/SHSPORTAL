"""Users model"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.models.base import DateTimeModelMixin, UserIDModelMixin, IsDeletedModelMixin


class UserBase(BaseModel):
    """User base model"""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    role_id: UUID = Field(...)
    school_id: Optional[UUID] = None


class UserCreate(UserBase):
    """User create model"""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update model"""

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role_id: Optional[UUID] = Field(None)
    school_id: Optional[UUID] = None

    class Config:
        """Configurations for the class."""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class UserInDb(UserCreate, IsDeletedModelMixin, UserIDModelMixin, DateTimeModelMixin):
    """User in DB model"""

    hashed_password: str


class UserPublic(UserBase, DateTimeModelMixin, UserIDModelMixin):
    """User public model"""

    pass
