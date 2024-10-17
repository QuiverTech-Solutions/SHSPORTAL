"""Model for Role."""

from typing import Optional

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class RoleBase(BaseModel):
    """Role Base Model."""

    name: str = Field(...)


class RoleCreate(RoleBase):
    """Role create model."""

    pass


class RoleInDb(RoleCreate, IDModelMixin_, DateTimeModelMixin, IsDeletedModelMixin):
    """Role in db model."""

    pass


class RolePublic(RoleCreate, DateTimeModelMixin, IDModelMixin_):
    """Role public model."""

    pass


class RoleUpdate(BaseModel):
    """Role update model."""

    name: Optional[str] = Field(...)

    class Config:
        """Configurations for the class."""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"
