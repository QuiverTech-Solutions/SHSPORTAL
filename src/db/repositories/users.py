"""Model for User."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.models.base import (
    UUID,
    DateTimeModelMixin,
    IsDeletedModelMixin,
    UserIDModelMixin,
)
from src.utils.validators import Validators


class UserStatus(str, Enum):
    """User status enum."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class UserBase(BaseModel):
    """User base model"""

    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    email: EmailStr = Field(...)
    phone_number: str
    referred_by: Optional[UUID] = Field(None)

    @field_validator("email")
    def email_to_lowercase(cls, value: str) -> str:
        """Converts email to lowercase"""
        return value.lower()

    class Config:
        """Configurations for the class."""

        from_attributes = True
        validate_assignment = True

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        """Validates phone number"""
        if not Validators.is_valid_phonenumber(value):
            raise ValueError("Invalid phone number")
        return value


class UserCreate(UserBase):
    """User create model"""

    password_hash: str = Field(...)


class UserPublic(UserBase, DateTimeModelMixin, UserIDModelMixin):
    """User Public model"""

    roles: set[str]
    referral_code: str
    referral_count: int
    successful_referral_count: int  # Generated >1000 cedis revenue
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class UserInDb(UserPublic, IsDeletedModelMixin):
    """User in Db model"""

    password_hash: str


class UserPublicWithOrganizationWithAffiliateUser(UserPublic):
    """User Public with Organization model"""

    organization_id: Optional[UUID]
    organization_name: Optional[str]
    affiliate_id: Optional[UUID]
    affiliate_code: Optional[str]


class UserUpdate(BaseModel):
    """User update model"""

    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    phone_number: Optional[str] = Field(None, min_length=9)
    email: EmailStr = Field(...)

    @field_validator("email")
    def email_to_lowercase(cls, value: str) -> str:
        """Converts email to lowercase"""
        return value.lower()

    class Config:
        """Configurations for the class."""

        from_attributes = True
        validate_assignment = True
        forbid = True