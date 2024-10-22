"""Token model."""

from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    """Token model"""

    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)
