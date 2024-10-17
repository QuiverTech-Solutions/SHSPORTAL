"""Settings model."""

from typing import Optional

from pydantic import BaseModel, Field

from src.models.base import DateTimeModelMixin, IDModelMixin_, IsDeletedModelMixin


class SettingsBase(BaseModel):
    """Settings base model."""

    key: str = Field(...)
    value: str = Field(...)


class SettingsCreate(SettingsBase):
    """Settings create model."""

    pass


class SettingsInDb(
    SettingsBase, DateTimeModelMixin, IsDeletedModelMixin, IDModelMixin_
):
    """Settings in db model."""

    pass


class SettingsPublic(SettingsBase, DateTimeModelMixin, IDModelMixin_):
    """Settings public model."""

    pass


class SettingsUpdate(BaseModel):
    """Settings update model."""

    key: Optional[str] = Field(None)
    value: Optional[str] = Field(None)

    class Config:
        """Configurations for the class."""

        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"
