"""Dependency for authentication."""

import logging
from typing import Tuple

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)
app_logger = logging.getLogger("app")


async def get_auth_service() -> AuthService:
    """Auth Service Dependency."""
    return AuthService()


# async def get_user_repository(db: Database = Depends(get_database)) -> UserRepository:
#     """User Repository Dependency."""
#     return UserRepository(db)


async def get_token_from_cookies(request: Request) -> Tuple[str, str]:
    """Get the access and refresh tokens from the cookies."""
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if not access_token or not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials. Token not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token, refresh_token


async def get_current_user(
    tokens: Tuple[str, str] = Depends(get_token_from_cookies),
) -> str:
    """Get the current user from the access token."""
    access_token, refresh_token = tokens
    return access_token


def get_event_participant_admin() -> None:
    """Get the event participant admin."""
    pass


def require_role(required_role: str) -> Depends:
    """Dependency to require a role for accessing a route."""

    async def wrapper() -> str:
        """Wrapper for requiring a role."""
        # Update this, this is just a placeholder
        return "This is the role details"

    return wrapper


get_super_admin = require_role("super_admin")
get_event_org_admin = require_role("event_org_admin")
