"""Dependency for authentication."""

import logging
from typing import Tuple

from databases import Database
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.database import get_database, get_repository
from src.db.repositories.refresh_token import RefreshTokenRepository
from src.db.repositories.user import UserRepository
from src.errors.database import IncorrectCredentialsError
from src.models.user import UserInDb, UserPublicWithOrganizationWithAffiliateUser
from src.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)
app_logger = logging.getLogger("app")


async def get_auth_service() -> AuthService:
    """Auth Service Dependency."""
    return AuthService()


async def get_user_repository(db: Database = Depends(get_database)) -> UserRepository:
    """User Repository Dependency."""
    return UserRepository(db)


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
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repository),
    refresh_token_repo: RefreshTokenRepository = Depends(
        get_repository(RefreshTokenRepository)
    ),
) -> UserPublicWithOrganizationWithAffiliateUser:
    """Get the current user from the access token."""
    access_token, refresh_token = tokens
    try:
        user_id = await auth_service.verify_token(access_token)
    except IncorrectCredentialsError:
        # Access token expired, try to use refresh token
        try:
            user_id = await auth_service.verify_token(refresh_token)
            active_token = await refresh_token_repo.get_active_refresh_token_by_user_id(
                user_id=user_id
            )
            if not active_token or active_token.token != refresh_token:
                await refresh_token_repo.deactivate_active_refresh_token_for_user(
                    user_id=user_id
                )
                raise HTTPException(  # noqa
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
        except Exception as e:
            app_logger.exception("Refresh token verification failed", exc_info=e)
            raise HTTPException(  # noqa
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
    except Exception as e:
        app_logger.exception("Access token verification failed", exc_info=e)
        raise HTTPException(  # noqa
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    user = await user_repo.get_user_with_organization_with_affiliate_user_by_user_id(
        user_id=user_id
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user


def get_event_participant_admin() -> None:
    """Get the event participant admin."""
    pass


def require_role(required_role: str) -> Depends:
    """Dependency to require a role for accessing a route."""

    async def wrapper(
        user: UserPublicWithOrganizationWithAffiliateUser = Depends(get_current_user),
    ) -> UserInDb:
        """Wrapper for requiring a role."""
        if required_role in user.roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )

    return wrapper


get_super_admin = require_role("super_admin")
get_event_org_admin = require_role("event_organizer")
get_affiliate_user = require_role("affiliate_user")
