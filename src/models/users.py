from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.models.base import DateTimeModelMixin, UserIDModelMixin, IsDeletedModelMixin


class UserBase(BaseModel):
    """User base model"""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(..., description="User's email address")
    role_id: UUID = Field(..., description="Role of the user")
    school_id: Optional[UUID] = None

    @field_validator("email")
    def email_to_lowercase(cls, value: str) -> str:
        """Converts email to lowercase"""
        return value.lower()

    class Config:
        """Configurations for the class."""
        from_attributes = True
        validate_assignment = True


class UserCreate(UserBase):
    """User create model (Sign-up)"""

    password: str = Field(..., min_length=8, description="User's password for signup")


class UserUpdate(BaseModel):
    """User update model"""

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role_id: Optional[UUID] = Field(None)
    school_id: Optional[UUID] = None

    @field_validator("email")
    def email_to_lowercase(cls, value: str) -> str:
        """Converts email to lowercase"""
        return value.lower()

    class Config:
        """Configurations for the class."""
        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


class UserInDb(UserCreate, IsDeletedModelMixin, UserIDModelMixin, DateTimeModelMixin):
    """User in DB model"""

    hashed_password: str


class UserPublic(UserBase, DateTimeModelMixin, UserIDModelMixin):
    """User public model (response model)"""

    pass


class UserLogin(BaseModel):
    """User login model"""

    email: EmailStr = Field(..., description="Email for login")
    password: str = Field(..., description="Password for login")

    @field_validator("email")
    def email_to_lowercase(cls, value: str) -> str:
        """Converts email to lowercase for consistency."""
        return value.lower()
