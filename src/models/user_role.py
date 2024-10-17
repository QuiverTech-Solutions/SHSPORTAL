"""Model for user roles."""

from pydantic import BaseModel, Field

from src.models.base import UUID, DateTimeModelMixin, IsDeletedModelMixin


class UserRolesBase(BaseModel):
    """User Roles Base Model."""

    user_id: UUID = Field(...)


class UserRolesCreate(UserRolesBase):
    """User Roles create model."""

    role_name: str = Field(...)


class UserRolesInDb(UserRolesBase, DateTimeModelMixin, IsDeletedModelMixin):
    """User Roles in db model."""

    role_id: UUID = Field(...)


class UserRolesPublic(UserRolesBase, DateTimeModelMixin):
    """User Roles public model."""

    role_id: UUID = Field(...)
